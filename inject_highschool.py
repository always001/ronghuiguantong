# -*- coding: utf-8 -*-
import os, re

# 路径相对化：脚本同级目录
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "js", "data.js")
s = open(p, encoding="utf-8").read()

# 注入模块的 (stage, grade) 统一映射：把"高中 · 专题·..."旧命名收敛为数字年级
INJECT_MAP = {
    "trig_id": ("高中", "十一年级"), "complex": ("高中", "十年级"), "seqsum": ("高中", "十一年级"),
    "deriv_mon": ("高中", "十二年级"), "deriv_ineq": ("高中", "十二年级"), "func_zero": ("高中", "十二年级"),
    "conic_link": ("高中", "十二年级"), "conic_chord": ("高中", "十二年级"), "conic_prop": ("高中", "十二年级"),
    "param_eq": ("高中", "十二年级"), "solid_axis": ("高中", "十一年级"), "solid_angle": ("高中", "十一年级"),
    "dist_exp": ("高中", "十二年级"), "dist_binom": ("高中", "十二年级"), "stat_case": ("高中", "十二年级"),
}
# 幂等守卫：这些 id 已存在则跳过注入，避免重复追加
already = [tid for tid in INJECT_MAP if ('id: "%s"' % tid) in s]
if already:
    print("已存在模块，跳过注入：", already)
    raise SystemExit(0)

def normalize_modules(text):
    """把每个注入模块里的 grade 旧命名改写为 (grade, stage) 数字年级写法。"""
    for tid, (stage, grade) in INJECT_MAP.items():
        m = re.search(r'\{\s*id:\s*"%s"' % re.escape(tid), text)
        if not m:
            continue
        seg = text[m.end():]
        text = text[:m.end()] + re.sub(r'grade:\s*"[^"]*"',
                'grade: "%s", stage: "%s"' % (grade, stage), seg, count=1)
    return text

modules = r'''
  /* ===================== 高中 · 专题·代数与函数 ===================== */
  {
    id: "trig_id", grade: "高中 · 专题·代数与函数", name: "三角恒等变换", anim: null,
    summary: "和差角、二倍角、辅助角公式，把复杂三角函数化简。",
    kou: "和角记口诀‘余余正正’，二倍角三形式等价，辅助角提根号配φ。",
    steps: [
      "<b>和差角</b>：sin(α±β)=sinαcosβ±cosαsinβ；cos(α±β)=cosαcosβ∓sinαsinβ。",
      "<b>二倍角</b>：sin2α=2sinαcosα；cos2α=cos²α−sin²α=2cos²α−1=1−2sin²α。",
      "<b>辅助角</b>：a·sinx+b·cosx=√(a²+b²)·sin(x+φ)，tanφ=b/a。"
    ],
    prereq: null,
    questions: [
      { q: "sin(α+β) 展开为？", opts: ["sinαcosβ+cosαsinβ","sinαsinβ+cosαcosβ","sinαcosβ−cosαsinβ","cosαcosβ−sinαsinβ"], ans: 0, level: "基础",
        explain: "和角公式 sin(α+β)=sinαcosβ+cosαsinβ。", point: "和角公式" },
      { q: "cos2α 的等价形式有几个？", opts: ["1 个","2 个","3 个","以上都对（三种均等价）"], ans: 3, level: "基础",
        explain: "cos2α=cos²α−sin²α=2cos²α−1=1−2sin²α，三种都对。", point: "二倍角" },
      { q: "sin²α+cos²α 等于？", opts: ["2","0","1","tanα"], ans: 2, level: "基础",
        explain: "同角平方关系恒为 1。", point: "基本关系" },
      { q: "a·sinx+b·cosx 可化为？", opts: ["√(a²+b²) sin(x+φ)","√(a²+b²) cos(x−φ)","两者均可","都不对"], ans: 2, level: "进阶",
        explain: "辅助角公式两种写法都成立，φ 由 tanφ=b/a 确定。", point: "辅助角" }
    ]
  },
  {
    id: "complex", grade: "高中 · 专题·代数与函数", name: "复数运算", anim: null,
    summary: "复数加减乘除、模与共轭，及在复平面的几何意义。",
    kou: "加减实虚各自算，乘法i²=−1，模是到原点距离，共轭改虚部符号。",
    steps: [
      "<b>加减</b>：实部与实部、虚部与虚部分别相加减。",
      "<b>乘法</b>：按多项式乘，注意 i²=−1。",
      "<b>模</b>：|a+bi|=√(a²+b²)；<b>共轭</b>：a+bi 的共轭为 a−bi。"
    ],
    prereq: null,
    questions: [
      { q: "(1+2i)+(3−i) = ?", opts: ["4+i","2+3i","4−i","3+2i"], ans: 0, level: "基础",
        explain: "实部 1+3=4，虚部 2i−i=i → 4+i。", point: "加减" },
      { q: "(1+i)² = ?", opts: ["1+2i","2i","2","−2i"], ans: 1, level: "基础",
        explain: "(1+i)²=1+2i+i²=1+2i−1=2i。", point: "乘法" },
      { q: "i 的幂：i¹=i, i²=−1, i³=−i, i⁴=1，则 i²⁰²⁵ = ?", opts: ["1","−1","−i","i"], ans: 3, level: "进阶",
        explain: "2025÷4 余 1，故 i²⁰²⁵=i。", point: "周期性" },
      { q: "复数 z=3+4i 的模 |z| = ?", opts: ["7","25","√7","5"], ans: 3, level: "基础",
        explain: "|3+4i|=√(3²+4²)=5。", point: "模" }
    ]
  },
  {
    id: "seqsum", grade: "高中 · 专题·代数与函数", name: "数列求和技巧", anim: null,
    summary: "等差×等比用错位相减，分式裂项相消，纯等比用求和公式。",
    kou: "等差乘等比→错位相减；相邻分母差1→裂项相消；纯等比→套公式。",
    steps: [
      "<b>错位相减</b>：S=qS 两式相减，构造等比数列求和（等差×等比）。",
      "<b>裂项相消</b>：1/[k(k+1)]=1/k−1/(k+1)，相加中间抵消。",
      "<b>等比求和</b>：S_n=a₁(1−qⁿ)/(1−q)（q≠1）。"
    ],
    prereq: null,
    questions: [
      { q: "错位相减法最适合哪类数列求和？", opts: ["纯等比数列","纯等差数列","等差×等比数列","常数列"], ans: 2, level: "基础",
        explain: "等差×等比数列求和用错位相减。", point: "适用" },
      { q: "1/2+1/6+1/12+…+1/[n(n+1)] 的和 = ?", opts: ["n/(n+1)","1/(n+1)","(n+1)/n","1/2"], ans: 0, level: "进阶",
        explain: "裂项相消：1−1/(n+1)=n/(n+1)。", point: "裂项" },
      { q: "等比数列求和公式 S_n=a₁(1−qⁿ)/(1−q) 要求？", opts: ["q=1","a₁=0","q≠1","n=1"], ans: 2, level: "基础",
        explain: "q=1 时退化为 na₁，公式要求 q≠1。", point: "等比求和" },
      { q: "1·2+2·2²+3·2³+…+n·2ⁿ 求和应优先用？", opts: ["裂项相消","分组求和","错位相减","倒序相加"], ans: 2, level: "进阶",
        explain: "等差(n)×等比(2ⁿ)→错位相减。", point: "错位" }
    ]
  },
  {
    id: "deriv_mon", grade: "高中 · 专题·代数与函数", name: "导数与单调性极值", anim: null,
    summary: "求导→令导数为零→列表判单调区间与极值。",
    kou: "先求定义域再求导，f'>0 递增 f'<0 递减，驻点两侧变号才取极值。",
    steps: [
      "求<b>定义域</b>，再求导 f'(x)。",
      "令 f'(x)=0 求<b>驻点</b>。",
      "列表判符号：f'>0 递增、f'<0 递减，驻点两侧变号得极值。"
    ],
    prereq: null,
    questions: [
      { q: "若 f'(x)>0 在区间 I 上恒成立，则 f(x) 在 I 上？", opts: ["单调递减","为常数","单调递增","先增后减"], ans: 2, level: "基础",
        explain: "导数正→函数单调递增。", point: "单调性" },
      { q: "f(x)=x³−3x 的驻点是？", opts: ["±1","0","0,±1","2"], ans: 0, level: "基础",
        explain: "f'=3x²−3=0 → x²=1 → x=±1。", point: "驻点" },
      { q: "求单调区间的第一步通常是？", opts: ["求导","令 f'=0","求定义域","画表格"], ans: 2, level: "基础",
        explain: "先确定定义域，再求导分析。", point: "步骤" },
      { q: "f(x)=e^x−x 的最小值在何处取得？", opts: ["x=1","x=−1","x=0","无最小值"], ans: 2, level: "进阶",
        explain: "f'=e^x−1=0→x=0，f''=e^x>0，x=0 取极小值也是最小值。", point: "极值" }
    ]
  },
  {
    id: "deriv_ineq", grade: "高中 · 专题·代数与函数", name: "导数与不等式恒成立", anim: null,
    summary: "恒成立问题转化为最值：f(x)≥0 恒成立 ⇔ f_min≥0。",
    kou: "恒成立看最值：f≥0⇔最小值≥0；含参先分离参数再求最值。",
    steps: [
      "将恒成立 a≤f(x) 转化为 a≤<b>f(x)最小值</b>。",
      "含参难以分离时，构造 g(x)=f(x)−kx，求 g_min≥0。",
      "用导数求最值，必要时讨论参数范围。"
    ],
    prereq: "deriv_mon",
    questions: [
      { q: "要证 f(x)≥0 对一切 x 恒成立，等价于 f(x) 的？", opts: ["最小值≥0","最大值≥0","最小值≤0","任意值均可"], ans: 0, level: "基础",
        explain: "恒成立 ⇔ 最小值≥0。", point: "转化" },
      { q: "若要使 f(x)≥a 恒成立，则参数 a 应满足？", opts: ["a≥f(x)最大值","a≤f(x)最小值","a=0","a≥1"], ans: 1, level: "基础",
        explain: "a 不超过 f 的最小值即可。", point: "分离参数" },
      { q: "分离参数法最适用于？", opts: ["多参数纠缠","参数在指数里","参数易分离","无法求导"], ans: 2, level: "进阶",
        explain: "参数易分离时优先分离，转化为最值问题。", point: "方法选择" },
      { q: "构造 g(x)=f(x)−kx，要 g(x)≥0 恒成立，应分析？", opts: ["g 的最大值≥0","g 的最小值≥0","g≡0","无需分析"], ans: 1, level: "进阶",
        explain: "仍转化为 g 的最小值≥0。", point: "构造" }
    ]
  },
  {
    id: "func_zero", grade: "高中 · 专题·代数与函数", name: "函数零点与极值点偏移", anim: null,
    summary: "零点即 f(x)=0 的解；极值点偏移用对称函数构造证明。",
    kou: "零点即方程解，连续+异号必有零点；偏移问题构造对称差函数。",
    steps: [
      "<b>零点</b>：f(x)=0 的实数解；存在定理——连续且 f(a)f(b)<0 则 (a,b) 内有零点。",
      "<b>个数</b>：用单调性+端点极限判断。",
      "<b>极值点偏移</b>：构造对称函数 F(x)=f(x₀+x)−f(x₀−x) 证偏移方向。"
    ],
    prereq: "deriv_mon",
    questions: [
      { q: "函数零点是？", opts: ["极值点","方程 f(x)=0 的实数解","导数","渐近线"], ans: 1, level: "基础",
        explain: "零点即 f(x)=0 的解。", point: "定义" },
      { q: "零点存在定理：f 连续且 f(a)f(b)<0，则 (a,b) 内？", opts: ["无零点","唯一零点","至少一个零点","恰两个零点"], ans: 2, level: "基础",
        explain: "至少存在一个零点。", point: "存在定理" },
      { q: "证明极值点偏移常用方法是构造？", opts: ["直接求导","积分","对称差函数","求极限"], ans: 2, level: "进阶",
        explain: "构造对称差函数证偏移方向。", point: "方法" },
      { q: "f(x)=x−e^(−x) 的零点个数为？", opts: ["0","2","无穷多","1"], ans: 3, level: "进阶",
        explain: "f'=1+e^(−x)>0 严格增，且 f(−∞)→−∞、f(∞)→∞，故恰 1 个零点。", point: "个数" }
    ]
  },
  /* ===================== 高中 · 专题·解析几何 ===================== */
  {
    id: "conic_link", grade: "高中 · 专题·解析几何", name: "联立与韦达定理", anim: "conic",
    summary: "直线与圆锥曲线联立得一元二次，用韦达定理得交点坐标关系。",
    kou: "联立消元得二次方程，和=−b/a、积=c/a，不解方程知关系。",
    steps: [
      "直线代入曲线，<b>消去 y</b> 得关于 x 的一元二次方程 ax²+bx+c=0。",
      "判别式 Δ>0 才有两交点。",
      "由<b>韦达定理</b>：x₁+x₂=−b/a，x₁x₂=c/a。"
    ],
    prereq: null,
    questions: [
      { q: "直线与二次曲线联立、消元后一般得到？", opts: ["一元一次方程","二元一次","一元二次方程","常数方程"], ans: 2, level: "基础",
        explain: "通常得到关于一个变量的一元二次方程。", point: "联立" },
      { q: "若 ax²+bx+c=0 两实根为 x₁,x₂，则 x₁+x₂ = ?", opts: ["−b/a","b/a","c/a","−c/a"], ans: 0, level: "基础",
        explain: "韦达和=−b/a。", point: "韦达和" },
      { q: "x₁·x₂ = ?", opts: ["−b/a","−c/a","c/a","b/c"], ans: 2, level: "基础",
        explain: "韦达积=c/a。", point: "韦达积" },
      { q: "求弦中点坐标常用？", opts: ["代入法","求导","点差法","积分"], ans: 2, level: "进阶",
        explain: "中点弦常用点差法。", point: "点差法" }
    ]
  },
  {
    id: "conic_chord", grade: "高中 · 专题·解析几何", name: "弦长·中点·定点定值", anim: "conic",
    summary: "弦长公式 √(1+k²)·|x₁−x₂|；过定点问题设含参直线找不变量。",
    kou: "弦长套公式，中点用点差，定点设含参直线令系数为零。",
    steps: [
      "<b>弦长</b>：|AB|=√(1+k²)·|x₁−x₂|，其中 |x₁−x₂|=√Δ/|a|。",
      "<b>中点弦</b>：点差法得 k₁·k₂=−b²/a²（椭圆）。",
      "<b>定点定值</b>：设含参直线，令参数系数为零求定点。"
    ],
    prereq: "conic_link",
    questions: [
      { q: "弦长公式里 |x₁−x₂| = ?", opts: ["Δ/a","√Δ","√Δ/|a|","Δ"], ans: 2, level: "基础",
        explain: "|x₁−x₂|=√Δ/|a|。", point: "弦长" },
      { q: "抛物线 y²=2px 的焦点坐标是？", opts: ["(p,0)","(p/2,0)","(0,p/2)","(2p,0)"], ans: 1, level: "基础",
        explain: "焦点为 (p/2,0)。", point: "焦点" },
      { q: "证明直线过定点，常把直线设为？", opts: ["x=常数","y=常数","y=kx+m（含参）","任意直线"], ans: 2, level: "进阶",
        explain: "设含参直线后令参数为零求定点。", point: "定点" },
      { q: "椭圆 x²/a²+y²/b²=1 中，弦中点与中心连线斜率 k₁、弦斜率 k₂ 满足？", opts: ["b²/a²","a²/b²","−b²/a²","−a²/b²"], ans: 2, level: "进阶",
        explain: "点差法得 k₁·k₂=−b²/a²。", point: "中点弦" }
    ]
  },
  {
    id: "conic_prop", grade: "高中 · 专题·解析几何", name: "圆锥曲线性质", anim: null,
    summary: "椭圆 e∈(0,1)、双曲线 e>1 且实轴 2a、抛物线到焦点与准线等距。",
    kou: "椭圆离心聚拢、双曲发散、抛物等距；e=c/a 定形状。",
    steps: [
      "<b>椭圆</b>：0<e<1，实轴短轴按 a、b 定。",
      "<b>双曲线</b>：e>1，实轴 2a，渐近线 y=±(b/a)x。",
      "<b>抛物线</b>：到焦点与准线距离相等。"
    ],
    prereq: null,
    questions: [
      { q: "椭圆的离心率 e=c/a 的范围是？", opts: ["e=1","e>1","0<e<1","e=0"], ans: 2, level: "基础",
        explain: "椭圆 0<e<1。", point: "离心率" },
      { q: "双曲线的实轴长为？", opts: ["2b","a","2a","c"], ans: 2, level: "基础",
        explain: "实轴长=2a。", point: "实轴" },
      { q: "抛物线的定义是到焦点与定直线？", opts: ["距离和定","距离差定","距离相等","无关"], ans: 2, level: "基础",
        explain: "抛物线=到焦点与准线距离相等。", point: "定义" },
      { q: "双曲线的离心率 e = ?", opts: ["a/c","b/a","1","c/a 且 e>1"], ans: 3, level: "基础",
        explain: "e=c/a 且双曲线 e>1。", point: "离心率" }
    ]
  },
  {
    id: "param_eq", grade: "高中 · 专题·解析几何", name: "参数方程与极坐标", anim: null,
    summary: "圆/椭圆用三角参数，直线用有向距离参数，极坐标描述圆与玫瑰线。",
    kou: "圆椭圆用 cos/sin 参数，直线参数 t 是有向距离，极坐标 ρ=2a cosθ 是圆。",
    steps: [
      "<b>圆</b>：x=Rcosθ, y=Rsinθ。",
      "<b>直线</b>：x=x₀+tcosα, y=y₀+tsinα，t 为点到起点的有向距离。",
      "<b>极坐标</b>：ρ=2a cosθ 表示圆，ρ=2a sinθ 也是圆。"
    ],
    prereq: "conic_prop",
    questions: [
      { q: "圆 x²+y²=R² 的标准参数方程是？", opts: ["x=Rθ, y=R","x=Rcosθ, y=Rsinθ","x=Rcos2θ","x=Rsinθ"], ans: 1, level: "基础",
        explain: "x=Rcosθ, y=Rsinθ。", point: "圆参数" },
      { q: "直线参数方程 x=x₀+tcosα, y=y₀+tsinα 中 t 表示？", opts: ["斜率","时间","有向距离","截距"], ans: 2, level: "基础",
        explain: "t 为点到起点的有向距离。", point: "直线参数" },
      { q: "极坐标方程 ρ=2a cosθ 表示？", opts: ["直线","双曲线","圆","抛物线"], ans: 2, level: "进阶",
        explain: "ρ=2a cosθ 是圆（圆心在 x 轴）。", point: "极坐标" },
      { q: "椭圆 x=a cosθ, y=b sinθ 中的 θ 是？", opts: ["极角","倾斜角","离心角（非几何转角）","方位角"], ans: 2, level: "进阶",
        explain: "θ 为离心角，一般不代表点的真实几何转角。", point: "离心角" }
    ]
  },
  /* ===================== 高中 · 专题·立体几何与概率 ===================== */
  {
    id: "solid_axis", grade: "高中 · 专题·立体几何与概率", name: "空间向量建系", anim: "solid",
    summary: "建立空间直角坐标系，用坐标与向量处理位置与度量。",
    kou: "建系让点落轴面，向量坐标即分量，模长用勾股定理。",
    steps: [
      "选互相垂直的三条线为 <b>x、y、z 轴</b>，交点为原点。",
      "尽量让更多点落在坐标轴或坐标平面上，简化坐标。",
      "点 P(x,y,z)，向量 a=(x,y,z)，模 |a|=√(x²+y²+z²)。"
    ],
    prereq: null,
    questions: [
      { q: "空间直角坐标系的三轴关系是？", opts: ["共面","互相平行","两两垂直","任意"], ans: 2, level: "基础",
        explain: "x、y、z 三轴两两垂直。", point: "三垂直" },
      { q: "建系时优先把哪些点落在坐标元素上？", opts: ["任意点","几何中心","坐标轴/坐标平面","顶点"], ans: 2, level: "基础",
        explain: "让更多点落在轴或面上，坐标更简。", point: "建系原则" },
      { q: "点 P(2,−1,3) 关于 xOy 平面对称的点是？", opts: ["(−2,1,3)","(2,1,3)","(2,−1,−3)","(−2,−1,−3)"], ans: 2, level: "进阶",
        explain: "关于 xOy 对称 → z 取反，得 (2,−1,−3)。", point: "对称" },
      { q: "向量 a=(1,2,3) 的模 |a| = ?", opts: ["14","6","√6","√14"], ans: 3, level: "基础",
        explain: "|a|=√(1+4+9)=√14。", point: "模" }
    ]
  },
  {
    id: "solid_angle", grade: "高中 · 专题·立体几何与概率", name: "空间角与距离", anim: "solid",
    summary: "线面角 sinθ=|cos<n,v>|；二面角看两法向量夹角或补角；点面距用投影。",
    kou: "线面角看方向向量与法向量夹角余弦；面距用点到面投影。",
    steps: [
      "<b>线面角</b> θ：sinθ=|cos<方向向量 v, 法向量 n>|。",
      "<b>二面角</b>：等于两平面法向量夹角或其补角（结合图形判断）。",
      "<b>点面距</b>：d=|PA·n|/|n|，n 为平面法向量。"
    ],
    prereq: "solid_axis",
    questions: [
      { q: "线面角 θ 满足 sinθ = ?（v 为直线方向，n 为平面法向量）", opts: ["|cos<n,v>|","|sin<n,v>|","cos<v,平面>","1"], ans: 0, level: "基础",
        explain: "sinθ=|cos<v,n>|。", point: "线面角" },
      { q: "二面角大小等于两平面法向量夹角的？", opts: ["和","两倍","夹角或其补角","一半"], ans: 2, level: "基础",
        explain: "二面角=法向量夹角或其补角。", point: "二面角" },
      { q: "点 P 到平面 α 的距离 d=|PA·n|/|n| 中 n 是？", opts: ["直线方向","任意向量","平面法向量","单位向量"], ans: 2, level: "基础",
        explain: "n 为平面 α 的法向量。", point: "点面距" },
      { q: "两平行平面间的距离可转化为？", opts: ["线面角","二面角","一面上任一点到另一面的距离","弦长"], ans: 2, level: "进阶",
        explain: "取一面上任一点求到另一面的距离。", point: "平行面距" }
    ]
  },
  {
    id: "dist_exp", grade: "高中 · 专题·立体几何与概率", name: "分布列与期望方差", anim: null,
    summary: "离散型随机变量：E(X)=Σx_i p_i，D(X)=E(X²)−[E(X)]²。",
    kou: "期望加权平均，方差看离散，线性 E(aX+b)=aE+b。",
    steps: [
      "列<b>分布列</b>，满足 p_i≥0 且 Σp_i=1。",
      "<b>期望</b> E(X)=Σx_i·p_i（加权平均）。",
      "<b>方差</b> D(X)=E(X²)−[E(X)]²，描述离散程度。"
    ],
    prereq: null,
    questions: [
      { q: "离散型随机变量期望 E(X) = ?", opts: ["Σp_i","Σx_i","max x_i","Σx_i·p_i"], ans: 3, level: "基础",
        explain: "E(X)=Σx_i·p_i。", point: "期望" },
      { q: "方差 D(X) 描述的是？", opts: ["集中趋势","平均值","离散程度","中位数"], ans: 2, level: "基础",
        explain: "方差描述数据离散程度。", point: "方差" },
      { q: "若 Y=aX+b，则 E(Y) = ?", opts: ["aE(X)","E(X)+b","aE(X)+b","a+b"], ans: 2, level: "进阶",
        explain: "期望的线性性质：E(aX+b)=aE(X)+b。", point: "线性" },
      { q: "任一分布列满足 Σp_i = ?", opts: ["0","E(X)","任意","1"], ans: 3, level: "基础",
        explain: "概率之和恒为 1。", point: "归一" }
    ]
  },
  {
    id: "dist_binom", grade: "高中 · 专题·立体几何与概率", name: "二项分布与正态分布", anim: null,
    summary: "X~B(n,p)：E=np, D=np(1−p)；正态分布关于 μ 对称。",
    kou: "二项分布看 n 次独立试验，正态看 μ 定位 σ 定胖瘦。",
    steps: [
      "<b>二项分布</b> B(n,p)：E=np，D=np(1−p)。",
      "<b>正态分布</b> N(μ,σ²)：关于 x=μ 对称。",
      "σ 越小曲线越瘦高，σ 越大越扁平。"
    ],
    prereq: "dist_exp",
    questions: [
      { q: "若 X~B(n,p)，则 E(X) = ?", opts: ["n(1−p)","p","n","np"], ans: 3, level: "基础",
        explain: "二项期望 E=np。", point: "二项期望" },
      { q: "若 X~B(n,p)，则 D(X) = ?", opts: ["np","n(1−p)","p(1−p)","np(1−p)"], ans: 3, level: "基础",
        explain: "二项方差 D=np(1−p)。", point: "二项方差" },
      { q: "正态分布曲线关于哪条线对称？", opts: ["反对称于原点","无对称","x=μ","随机平移"], ans: 2, level: "基础",
        explain: "关于均值 μ 对称。", point: "正态对称" },
      { q: "正态分布 N(μ,σ²) 中 σ 决定？", opts: ["位置","均值","曲线的胖瘦（离散程度）","面积"], ans: 2, level: "进阶",
        explain: "σ 越小越瘦高。", point: "σ意义" }
    ]
  },
  {
    id: "stat_case", grade: "高中 · 专题·立体几何与概率", name: "统计案例", anim: null,
    summary: "线性回归用最小二乘法；独立性检验用 χ² 统计量。",
    kou: "回归最小二乘求直线，独立性看 χ²，相关看 r 与 R²。",
    steps: [
      "<b>回归</b>：最小二乘法求 a、b，使残差平方和最小。",
      "<b>独立性检验</b>：列联表算 χ²，越大越拒绝独立。",
      "相关系数 r、决定系数 R² 越接近 1 拟合越好。"
    ],
    prereq: "dist_binom",
    questions: [
      { q: "线性回归求系数 a、b 用？", opts: ["取平均","令导数为零","最小二乘法","枚举"], ans: 2, level: "基础",
        explain: "最小二乘法。", point: "回归" },
      { q: "列联表独立性检验用？", opts: ["t 检验","F 检验","χ² 统计量","相关系数"], ans: 2, level: "基础",
        explain: "独立性检验用 χ²。", point: "独立性" },
      { q: "相关系数 r 越接近 1 表示？", opts: ["无相关","负相关","正线性相关越强","无关"], ans: 2, level: "基础",
        explain: "|r|→1 线性相关越强，r>0 为正相关。", point: "相关性" },
      { q: "样本决定系数 R² 越接近 1 表示模型？", opts: ["拟合越差","无关","过拟合","拟合越好"], ans: 3, level: "进阶",
        explain: "R²→1 拟合优度越高。", point: "拟合" }
    ]
  },
'''

# 注入：把现有最后一个技巧对象的 `}` 后加逗号，再插入新模块，最后以 `];` 收尾
modules = normalize_modules(modules)
marker = "  }\n];"
assert marker in s, "marker not found"
new_tail = "  },\n" + modules + "];"
s = s.replace(marker, new_tail, 1)

open(p, "w", encoding="utf-8").write(s)

# 校验
import re
print("total techniques:", s.count('id: "'))
print("grades:", dict(__import__("collections").Counter(re.findall(r'grade:\s*"([^"]+)"', s))))
# 简单校验每题 ans 在 0..3 且 opts 长度4
bad = []
for m in re.finditer(r'opts:\s*\[(.*?)\],\s*ans:\s*(\d+)', s, re.S):
    opts = m.group(1).count('"')
    ans = int(m.group(2))
    if opts != 4 or not (0 <= ans <= 3):
        bad.append((opts, ans))
print("opt-count/ans issues:", bad[:5], "total suspicious:", len(bad))
