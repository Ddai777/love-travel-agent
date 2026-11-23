"""
Agent Tools — 情侣出行决策 Agent 工具集（私有模块，不以 _ 开头暴露为路由）

所有工具定义都在这里。工具函数体是唯一需要改动的地方：把 mock 换成真实
实现即可。本Agent的核心工具全部走高德地图 Web 服务 API，Key 从环境变量
AMAP_API_KEY 读取（本地放 .env，线上放 EdgeOne Makers 环境变量）。
"""

import json
import os
import re
from typing import Annotated

import httpx
from agents import function_tool

AMAP_BASE = "https://restapi.amap.com"
REQUEST_TIMEOUT = 20.0


# ---------- 内部工具函数 ----------
def _amap_key() -> str:
    return os.getenv("AMAP_API_KEY", "").strip()


def _call_amap(path: str, params: dict) -> str:
    """统一调用高德 Web 服务 API，集中处理 Key 缺失 / 网络错误 / 业务错误。"""
    key = _amap_key()
    if not key:
        return json.dumps(
            {
                "ok": False,
                "error": (
                    "AMAP_API_KEY 未配置。请在本地 .env 或 EdgeOne Makers 控制台"
                    "配置高德地图 Key 后重试。"
                ),
            },
            ensure_ascii=False,
        )

    query = {"key": key, "output": "JSON", **params}
    try:
        resp = httpx.get(f"{AMAP_BASE}{path}", params=query, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:  # noqa: BLE001 - 工具层需要把任何异常回传给 Agent
        return json.dumps(
            {"ok": False, "error": f"地图服务请求失败：{type(exc).__name__}: {exc}"},
            ensure_ascii=False,
        )

    if str(data.get("status")) != "1":
        return json.dumps(
            {
                "ok": False,
                "error": (
                    f"地图服务返回错误：{data.get('info', '未知错误')} "
                    f"(infocode={data.get('infocode', '-')})"
                ),
            },
            ensure_ascii=False,
        )
    return json.dumps({"ok": True, **data}, ensure_ascii=False)


def _simplify_poi(poi: dict) -> dict:
    """裁剪高德 POI 字段，只把对推荐有用的信息交给大模型，节省 token。"""
    return {
        "name": poi.get("name"),
        "address": poi.get("address"),
        "location": poi.get("location"),
        "distance": poi.get("distance"),
        "businessArea": poi.get("businessarea"),
        "category": poi.get("typename"),
        "id": poi.get("id"),
    }


def _no_result(keywords: str) -> str:
    return json.dumps(
        {
            "ok": True,
            "count": 0,
            "message": f"没有搜到与“{keywords}”相关的地点，建议放宽关键词或扩大搜索范围。",
        },
        ensure_ascii=False,
    )


# ========== Tool 1: 地理编码 ==========
@function_tool
def geocode_address(
    address: Annotated[
        str, "要解析的地点名称或地址，例如“红莲南路地铁站”或“上海市静安区大悦城”"
    ],
    city: Annotated[str, "限定城市名称，可留空，例如“北京”"] = "",
) -> str:
    """把用户口述的文字地点解析成经纬度坐标。当用户给出的是文字地点（而非经纬度）时，必须先用本工具转换，再做周边搜索或距离计算。"""
    raw = _call_amap("/v3/geocode/geo", {"address": address, "city": city})
    data = json.loads(raw)
    if not data.get("ok"):
        return raw

    geocodes = data.get("geocodes") or []
    if not geocodes:
        return json.dumps(
            {
                "ok": False,
                "error": f"未能解析地点“{address}”，请用户提供更具体的地址或城市名。",
            },
            ensure_ascii=False,
        )

    results = [
        {
            "formattedAddress": g.get("formatted_address"),
            "location": g.get("location"),
            "city": g.get("city"),
            "district": g.get("district"),
        }
        for g in geocodes[:5]
    ]
    return json.dumps({"ok": True, "results": results}, ensure_ascii=False)


# ========== Tool 2: 关键词搜索商场 ==========
@function_tool
def search_malls_by_keyword(
    keywords: Annotated[
        str, "搜索关键词，如“商场”“购物中心”，或品牌名如“倍轻松”“西厅村屋”"
    ],
    city: Annotated[str, "城市名称，如“北京”；留空则全国搜索"] = "",
) -> str:
    """按关键词在城市里搜索商场或店铺，返回名称、地址、经纬度、所属商圈和类别。适合用户给出品牌偏好或想找某类商场时使用。"""
    raw = _call_amap(
        "/v3/place/text",
        {
            "keywords": keywords,
            "city": city,
            "citylimit": "true" if city else "false",
            "offset": 25,
            "page": 1,
        },
    )
    data = json.loads(raw)
    if not data.get("ok"):
        return raw

    pois = data.get("pois") or []
    if not pois:
        return _no_result(keywords)

    results = [_simplify_poi(p) for p in pois[:15]]
    return json.dumps(
        {"ok": True, "count": len(pois), "pois": results}, ensure_ascii=False
    )


# ========== Tool 3: 周边搜索商场 ==========
@function_tool
def search_nearby_malls(
    location: Annotated[
        str, "中心点经纬度，格式“经度,纬度”，由 geocode_address 得到，例如“116.390,39.910”"
    ],
    keywords: Annotated[str, "搜索关键词，如“商场”；留空表示搜索周边全部 POI"] = "商场",
    radius: Annotated[int, "搜索半径（米），默认 3000"] = 3000,
) -> str:
    """以给定经纬度为中心搜索附近的商场或店铺，结果按距离由近到远排序。适合用户说“我附近有啥商场”时使用。"""
    raw = _call_amap(
        "/v3/place/around",
        {
            "location": location,
            "keywords": keywords,
            "radius": radius,
            "sort": "distance",
            "offset": 25,
            "page": 1,
        },
    )
    data = json.loads(raw)
    if not data.get("ok"):
        return raw

    pois = data.get("pois") or []
    if not pois:
        return _no_result(keywords)

    results = [_simplify_poi(p) for p in pois[:15]]
    return json.dumps(
        {
            "ok": True,
            "center": location,
            "radius": radius,
            "count": len(pois),
            "pois": results,
        },
        ensure_ascii=False,
    )


# ========== Tool 4: 距离计算 ==========
@function_tool
def get_distance(
    origin: Annotated[str, "起点经纬度，格式“经度,纬度”，通常是用户当前位置"],
    destination: Annotated[
        str, "终点经纬度，格式“经度,纬度”；多个终点可用英文竖线 | 分隔"
    ],
    mode: Annotated[
        str, "出行方式：0=直线距离，1=驾车，2=步行，3=骑行；默认 1"
    ] = "1",
) -> str:
    """计算起点到商场等终点的距离（米）与预计耗时（秒），用于比较候选商场哪个更近。传入的必须是经纬度，不是地址文字。"""
    raw = _call_amap(
        "/v3/distance",
        {"origins": origin, "destination": destination, "type": mode},
    )
    data = json.loads(raw)
    if not data.get("ok"):
        return raw

    results = [
        {
            "distanceMeters": r.get("distance"),
            "durationSeconds": r.get("duration"),
        }
        for r in (data.get("results") or [])
    ]
    return json.dumps({"ok": True, "results": results}, ensure_ascii=False)


# ========== Tool 5: 天气查询（出行辅助，示例 mock） ==========
@function_tool
def get_weather(city: Annotated[str, "要查询天气的城市"]) -> str:
    """查询指定城市的当前天气，用于给出出行穿着建议。此工具为示例数据，可替换为真实天气 API。"""
    mock_weather = {
        "city": city,
        "condition": "Sunny",
        "temperature": {"min": 18, "max": 25, "unit": "°C"},
        "wind": "Light breeze",
        "note": "示例数据：接入真实天气服务后替换此处。",
    }
    return json.dumps(mock_weather, ensure_ascii=False)
