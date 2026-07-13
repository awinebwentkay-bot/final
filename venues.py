"""场地资源数据 — 来源于《场地资源.pdf》，作为场地推荐的唯一参考。"""

# 每个场地条目：名称、容量、设施、管理部门、位置、备注
Venue = dict

# ── 研读 / 研讨间（C楼三层） ──────────────────────────────
C_LOUNGE: list[Venue] = [
    {"name": "C207A", "capacity": 4, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C207B", "capacity": 4, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C207C", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C208A", "capacity": 4, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C208B", "capacity": 4, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C208C", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C209A", "capacity": 4, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C209B", "capacity": 2, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C210A", "capacity": 2, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C210B", "capacity": 2, "facilities": "小圆桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C212A", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C212B", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C213A", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C213B", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C214A", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C214B", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C215", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C221A", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C221B", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C307B", "capacity": 13, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C307A", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C310A", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C310B", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C311A", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C311B", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C311C", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C311D", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C321A", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C321B", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C321C", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C322A", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C322B", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C322C", "capacity": 2, "facilities": "小圆桌", "manager": "学课活", "location": "C楼三层", "note": ""},
    {"name": "C323A", "capacity": 9, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C324", "capacity": 11, "facilities": "会议桌；电源；电视（供投影）", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
]

# ── 校级公共教室研讨间 ────────────────────────────────────
SCHOOL_LOUNGE: list[Venue] = [
    {"name": "四教研讨间", "capacity": "3-4", "facilities": "桌椅", "manager": "教务处", "location": "四教", "note": "共11间；至少提前2小时申请，最多提前2周"},
    {"name": "建华楼研讨间", "capacity": "3-12", "facilities": "桌椅", "manager": "教务处", "location": "建华楼", "note": "共33间；至少提前2小时申请，最多提前2周"},
]

# ── 学生公寓活动空间（研讨/讨论间） ──────────────────────
DORM_LOUNGE: list[Venue] = [
    {"name": "31号楼社区活动中心B1讨论室", "capacity": 10, "facilities": "桌椅", "manager": "社区中心", "location": "31号楼B1", "note": "面向全校同学"},
]

# ── 活动室（C楼二层、三层） ───────────────────────────────
C_ACTIVITY: list[Venue] = [
    {"name": "C200", "capacity": 30, "facilities": "电视，投影幕布", "manager": "学课活", "location": "C楼二层", "note": "大型空场地，开放式空间，非密闭空间"},
    {"name": "C211（排练室）", "capacity": 30, "facilities": "大型空场地，电视，投影幕布", "manager": "学课活", "location": "C楼二层", "note": "可用于日常文艺活动"},
    {"name": "C212A", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C212B", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C213A", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C213B", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C214A", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C214B", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C215", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室"},
    {"name": "C217", "capacity": 20, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "开放式空间，优先支持班团活动"},
    {"name": "C218A", "capacity": 11, "facilities": "监视器、灯光控制台、绿幕、提词器、录像机", "manager": "学课活", "location": "C楼二层", "note": "导播室、演播室"},
    {"name": "C218B", "capacity": 11, "facilities": "电容麦克风、声卡", "manager": "学课活", "location": "C楼二层", "note": "录音室"},
    {"name": "C218C", "capacity": 11, "facilities": "监视器、灯光控制台、绿幕、提词器、录像机", "manager": "学课活", "location": "C楼二层", "note": "导播室、演播室"},
    {"name": "C218D", "capacity": 11, "facilities": "电容麦克风、声卡", "manager": "学课活", "location": "C楼二层", "note": "录音室"},
    {"name": "C221A", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C221B", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼二层", "note": "可用作会议室；A,B房间可合并使用，需单独分开借用"},
    {"name": "C307A", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C307B", "capacity": 13, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C309（排练室）", "capacity": 43, "facilities": "大型空场地，投影幕布", "manager": "学课活", "location": "C楼三层", "note": "可用于日常文艺活动"},
    {"name": "C310A", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C310B", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C319", "capacity": 25, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C320", "capacity": 33, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C323A", "capacity": 9, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C323B（排练室）", "capacity": 10, "facilities": "小型空场地，坐垫", "manager": "学课活", "location": "C楼三层", "note": "可用于日常文艺活动"},
    {"name": "C324", "capacity": 11, "facilities": "桌椅，屏幕", "manager": "学课活", "location": "C楼三层", "note": "可用作会议室"},
    {"name": "C325（排练室）", "capacity": 25, "facilities": "大型空场地，电视", "manager": "学课活", "location": "C楼三层", "note": "可用于日常文艺活动"},
]

# ── 南区地下活动室 ────────────────────────────────────────
SOUTH_BASEMENT: list[Venue] = [
    {"name": "B112", "capacity": 40, "facilities": "会议室；多功能厅；大屏幕；音响", "manager": "学课活", "location": "南区地下", "note": "需先通过学生活动申请平台申请，通过后再通过学生清华小程序预约"},
    {"name": "M02", "capacity": 20, "facilities": "功能椅", "manager": "学课活", "location": "南区地下", "note": ""},
    {"name": "M01", "capacity": 15, "facilities": "功能椅", "manager": "学课活", "location": "南区地下", "note": ""},
    {"name": "B206", "capacity": 15, "facilities": "舞蹈；镜子；智能电视", "manager": "学课活", "location": "南区地下", "note": "可用于日常文艺活动"},
    {"name": "B231", "capacity": 15, "facilities": "舞蹈；镜子；智能电视", "manager": "学课活", "location": "南区地下", "note": "可用于日常文艺活动"},
    {"name": "B210", "capacity": 10, "facilities": "功能椅；电视", "manager": "学课活", "location": "南区地下", "note": ""},
    {"name": "B211", "capacity": 10, "facilities": "功能椅", "manager": "学课活", "location": "南区地下", "note": ""},
]

# ── 校级公共教室 ──────────────────────────────────────────
SCHOOL_CLASSROOM: list[Venue] = [
    {"name": "一教教室", "capacity": 40, "facilities": "远程交互；录播；可移动桌椅", "manager": "教务处", "location": "一教", "note": "共5间；至少提前5天申请，最多提前2周"},
    {"name": "三教一段教室", "capacity": "12-82", "facilities": "远程交互；录播；部分可移动桌椅", "manager": "教务处", "location": "三教", "note": "共30间"},
    {"name": "三教三段教室", "capacity": "14-132", "facilities": "远程交互；录播；部分可移动桌椅；20间语音教室；2间专用教室", "manager": "教务处", "location": "三教", "note": "共47间"},
    {"name": "四教教室", "capacity": 60, "facilities": "远程交互；录播；部分可移动桌椅", "manager": "教务处", "location": "四教", "note": "共24间"},
    {"name": "五教教室", "capacity": "102-142", "facilities": "部分可移动桌椅", "manager": "教务处", "location": "五教", "note": "共11间"},
    {"name": "六教A区教室", "capacity": "24-180", "facilities": "部分可移动桌椅", "manager": "教务处", "location": "六教", "note": "共54间"},
    {"name": "六教B区教室", "capacity": 40, "facilities": "可移动桌椅", "manager": "教务处", "location": "六教", "note": "共42间"},
    {"name": "清华学堂教室", "capacity": "23-70", "facilities": "专用教室8间；部分可移动桌椅；2间可远程交互和录播", "manager": "教务处", "location": "清华学堂", "note": "共18间"},
    {"name": "新水利馆教室", "capacity": "25-180", "facilities": "远程交互；录播；部分可移动桌椅；14间绘图教室", "manager": "教务处", "location": "新水利馆", "note": "共21间"},
    {"name": "旧水利馆教室", "capacity": "38-96", "facilities": "远程交互；录播；绘图教室", "manager": "教务处", "location": "旧水利馆", "note": "共6间"},
    {"name": "法律图书馆教室", "capacity": "30-116", "facilities": "远程交互；录播；部分可移动桌椅；2间案例教室", "manager": "教务处", "location": "法律图书馆", "note": "共13间"},
    {"name": "明理楼教室", "capacity": "60-332", "facilities": "部分可移动桌椅", "manager": "教务处", "location": "明理楼", "note": "共5间"},
    {"name": "建华/经管新楼教室", "capacity": "36-264", "facilities": "桌椅；多媒体", "manager": "教务处", "location": "建华/经管新楼", "note": "共39间"},
    {"name": "建华/经管新楼公共区", "capacity": 80, "facilities": "桌椅", "manager": "教务处", "location": "建华/经管新楼", "note": ""},
]

# ── 会议室 ──────────────────────────────────────────────────
MEETING_ROOM: list[Venue] = [
    {"name": "胜因院22号会议室", "capacity": 20, "facilities": "触屏设备；椅子", "manager": "学生全球胜任力发展指导中心", "location": "胜因院22号", "note": "关注清华大学国际教育公众号预约"},
    {"name": "FIT楼4-302", "capacity": 20, "facilities": "有投影仪", "manager": "物业", "location": "FIT楼", "note": "主要面向FIT楼各使用单位在职教师，收费使用"},
]

# ── 图书馆音乐/研讨空间 ──────────────────────────────────
LIBRARY: list[Venue] = [
    {"name": "图书馆音乐讲堂", "capacity": 63, "facilities": "投影；高品质音响；钢琴", "manager": "图书馆", "location": "图书馆", "note": "需填写申请表发送至指定邮箱"},
    {"name": "西馆高山音乐研讨间（中208）", "capacity": 18, "facilities": "座椅，音响", "manager": "图书馆", "location": "西馆", "note": "至少需要5人预约；通过图书馆研讨间预约系统申请"},
    {"name": "西馆流水音乐研讨间（中210）", "capacity": 9, "facilities": "座椅，音响", "manager": "图书馆", "location": "西馆", "note": "至少需要3人预约；通过图书馆研讨间预约系统申请"},
    {"name": "北馆邺架轩交流区", "capacity": 40, "facilities": "用于交流", "manager": "图书馆", "location": "北馆", "note": "填写申请表发送至指定邮箱"},
]

# ── 学生公寓休闲空间 ──────────────────────────────────────
DORM_LOUNGE_REC: list[Venue] = [
    {"name": "31号楼社区活动中心B1休闲区", "capacity": 26, "facilities": "沙发；桌椅；书架", "manager": "社区中心", "location": "31号楼B1", "note": "面向全校同学"},
    {"name": "31号楼社区活动中心B1休闲水吧", "capacity": 4, "facilities": "自助贩卖机；桌椅", "manager": "社区中心", "location": "31号楼B1", "note": "面向全校同学"},
    {"name": "31号楼社区活动中心B1影音室", "capacity": 5, "facilities": "沙发；桌子", "manager": "社区中心", "location": "31号楼B1", "note": "面向全校同学"},
    {"name": "8号楼社区活动中心B1综合区（休息区）", "capacity": 18, "facilities": "沙发；桌子", "manager": "社区中心", "location": "8号楼B1", "note": "面向全校同学"},
]

# ── 其他空间 ──────────────────────────────────────────────
OTHER: list[Venue] = [
    {"name": "胜因院22号咖啡吧", "capacity": 6, "facilities": "咖啡机；冰箱；消毒柜；吧台；高脚凳", "manager": "全胜中心", "location": "胜因院22号", "note": "关注清华大学国际教育公众号预约"},
    {"name": "胜因院22号会客室", "capacity": 12, "facilities": "沙发；桌椅", "manager": "全胜中心", "location": "胜因院22号", "note": "关注清华大学国际教育公众号预约"},
    {"name": "胜因院22号门厅", "capacity": "16-20", "facilities": "桌椅", "manager": "全胜中心", "location": "胜因院22号", "note": "关注清华大学国际教育公众号预约"},
    {"name": "胜因院22号茶室", "capacity": 10, "facilities": "桌椅；橱柜", "manager": "全胜中心", "location": "胜因院22号", "note": "关注清华大学国际教育公众号预约"},
]

# ── 所有场地汇总 ──────────────────────────────────────────
ALL_VENUES: list[Venue] = (
    C_LOUNGE + SCHOOL_LOUNGE + DORM_LOUNGE + C_ACTIVITY
    + SOUTH_BASEMENT + SCHOOL_CLASSROOM + MEETING_ROOM
    + LIBRARY + DORM_LOUNGE_REC + OTHER
)


def recommend_venues(people: int) -> list[Venue]:
    """根据参与人数推荐合适的场地，返回按容量排序的推荐列表。"""
    def _parse_cap(cap: int | str) -> int:
        """取容量范围的上限作为排序依据。"""
        if isinstance(cap, int):
            return cap
        if isinstance(cap, str) and "-" in cap:
            return int(cap.split("-")[1])
        return int(cap)

    candidates = []
    for v in ALL_VENUES:
        cap = v["capacity"]
        if isinstance(cap, int):
            if cap >= people:
                candidates.append(v)
        elif isinstance(cap, str) and "-" in cap:
            parts = cap.split("-")
            if int(parts[1]) >= people:
                candidates.append(v)

    candidates.sort(key=lambda v: _parse_cap(v["capacity"]))
    return candidates[:5]  # 返回最匹配的 5 个