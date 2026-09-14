/* ============================================================
 * 融会贯通 · 初中数学方法参数化出题引擎
 * 覆盖：有理数、整式、一元一次方程、不等式、方程组、
 *       线段角、三角形、全等三角形、相似三角形、勾股定理、
 *       四边形、圆、一次函数、反比例函数、二次函数
 * ============================================================ */
(function () {
  const K = { ink: "#334155", sub: "#64748b", line: "#cbd5e1", pri: "#2f6fed", ok: "#16a34a", warn: "#d97706", red: "#dc2626", soft: "#eef3ff", blue: "#2563eb" };
  function S(w, h, inner) { return `<svg viewBox="0 0 ${w} ${h}" width="100%" style="max-width:${w}px;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">${inner}</svg>`; }
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); const t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  // opts(ans, make1, make2, make3) - 由正确答和3个干扰项生成4个互异选项
  function opts(ans, make1, make2, make3) {
    const arr = [String(ans), String(make1()), String(make2()), String(make3())];
    const unique = [...new Set(arr)];
    while (unique.length < 4) { unique.push(String(ans + unique.length)); }
    return { opts: unique.map(String), ans: unique.indexOf(String(ans)) };
  }

  function Q(q, optsObj, level, explain, point, fig) {
    return Object.assign({ q, level: level || "基础", explain, point: point || "" }, optsObj, { fig: fig || null });
  }

  /* ============================================================
   * 1. 有理数与数轴（七年级）
   * ============================================================ */
  function qRational(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 绝对值计算
        const a = rnd(-9, 9);
        const absA = Math.abs(a);
        o = opts(absA, () => -absA, () => rnd(-10, 10), () => 0);
        q = `|${a}| = ？`;
        exp = `绝对值表示数轴上点到原点的距离，|${a}| = ${absA}。`;
      } else if (type === 1) {
        // 相反数
        const a = rnd(-9, 9);
        const opp = -a;
        o = opts(opp, () => a, () => 0, () => rnd(-10, 10));
        q = `${a} 的相反数是？`;
        exp = `相反数只变符号，${a} 的相反数是 ${opp}。`;
      } else {
        // 大小比较
        const a = rnd(-5, -1);
        const b = rnd(1, 5);
        o = opts(b, () => a, () => 0, () => rnd(-6, 6));
        q = `比较 ${a} 与 ${b}，较大的是？`;
        exp = `正数大于负数，${b} > ${a}，较大的是 ${b}。`;
      }
      results.push(Q(q, o, "基础", exp, "有理数基础"));
    }
    return results;
  }

  /* ============================================================
   * 2. 整式加减（七年级）
   * ============================================================ */
  function qIntegral(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 合并同类项
        const a1 = rnd(1, 8), a2 = rnd(1, 8);
        const sum = a1 + a2;
        o = opts(`${sum}x`, () => `${a1 + a2 + 1}x`, () => `${a1}x`, () => `${a2}x`);
        q = `${a1}x + ${a2}x = ？`;
        exp = `同类项合并：系数相加 ${a1} + ${a2} = ${sum}，字母不变。`;
      } else if (type === 1) {
        // 去括号
        const a = rnd(1, 5);
        const b = rnd(1, 9);
        o = opts(`-${a}x + ${b}`, () => `-${a}x - ${b}`, () => `${a}x + ${b}`, () => `${a}x - ${b}`);
        q = `−(${a}x − ${b}) = ？`;
        exp = `括号前是负号，去括号后各项变号：−${a}x + ${b}。`;
      } else {
        // 系数识别
        const a = rnd(2, 9);
        o = opts(`${-a}`, () => `${a}`, () => `${a + 1}`, () => `1`);
        q = `单项式 −${a}x² 的系数是？`;
        exp = `单项式的系数是数字因数，−${a}x² 的系数是 ${-a}。`;
      }
      results.push(Q(q, o, "基础", exp, "整式加减"));
    }
    return results;
  }

  /* ============================================================
   * 3. 一元一次方程（七年级）
   * ============================================================ */
  function qLinear(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 4;
      let q, ans, o, exp;
      if (type === 0) {
        // 简单方程 ax + b = c
        const x = rnd(1, 10);
        const a = rnd(2, 5);
        const b = rnd(1, 10);
        const c = a * x + b;
        o = opts(x, () => x + 1, () => x - 1, () => rnd(1, 12));
        q = `${a}x + ${b} = ${c}，x = ？`;
        exp = `移项：${a}x = ${c} − ${b} = ${c - b}，x = ${c - b} ÷ ${a} = ${x}。`;
      } else if (type === 1) {
        // 去括号方程
        const x = rnd(1, 8);
        const a = rnd(2, 4);
        const b = rnd(1, 6);
        const c = a * (x + b);
        o = opts(x, () => x + 1, () => x - 1, () => rnd(1, 10));
        q = `${a}(x + ${b}) = ${c}，x = ？`;
        exp = `去括号：x + ${b} = ${c} ÷ ${a} = ${c / a}，x = ${c / a} − ${b} = ${x}。`;
      } else if (type === 2) {
        // 应用题（年龄问题）
        const age = rnd(8, 15);
        const years = rnd(5, 15);
        const fatherAge = 2 * age + years; // 保证 fatherAge > 2*age，x = years 为正解
        o = opts(years, () => years + 2, () => years - 2, () => years + 5);
        q = `儿子 ${age} 岁，父亲 ${fatherAge} 岁，几年后父亲年龄是儿子的 2 倍？`;
        exp = `设 x 年后：${fatherAge} + x = 2(${age} + x)，解得 x = ${years}。`;
      } else {
        // 分式方程
        const x = rnd(2, 8);
        const a = rnd(2, 5);
        const b = a * x;
        o = opts(x, () => x + 1, () => x - 1, () => rnd(1, 10));
        q = `${b} ÷ x = ${a}，x = ？`;
        exp = `x = ${b} ÷ ${a} = ${x}。`;
      }
      results.push(Q(q, o, type < 2 ? "基础" : "进阶", exp, "一元一次方程"));
    }
    return results;
  }

  /* ============================================================
   * 4. 一元一次不等式（七年级）
   * ============================================================ */
  function qInequal(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 2;
      let q, ans, o, exp;
      if (type === 0) {
        // 解不等式
        const x = rnd(2, 8);
        const a = rnd(2, 5);
        const b = rnd(1, 10);
        const c = a * x + b;
        o = opts(`x < ${x}`, () => `x > ${x}`, () => `x ≤ ${x}`, () => `x ≥ ${x}`);
        q = `解不等式 ${a}x + ${b} < ${c}，解集是？`;
        exp = `移项：${a}x < ${c} − ${b} = ${c - b}，x < ${c - b} ÷ ${a} = ${x}。`;
      } else {
        // 判断不等号方向
        const a = rnd(1, 5);
        const b = rnd(1, 9);
        const c = a * rnd(1, 3) + b + 5;
        o = opts(`x < ${(c - b) / a}`, () => `x > ${(c - b) / a}`, () => `x < ${((c - b) / a) + 1}`, () => `x > ${((c - b) / a) - 1}`);
        q = `解不等式 ${a}x + ${b} < ${c}，解集是？`;
        exp = `移项：${a}x < ${c - b}，x < ${(c - b) / a}。`;
      }
      results.push(Q(q, o, "基础", exp, "一元一次不等式"));
    }
    return results;
  }

  /* ============================================================
   * 5. 二元一次方程组（七年级）
   * ============================================================ */
  function qSystem(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 代入法
        const x = rnd(1, 8);
        const y = rnd(1, 8);
        const a1 = rnd(1, 3), b1 = rnd(1, 3);
        const c1 = a1 * x + b1 * y;
        const a2 = rnd(1, 3), b2 = rnd(1, 3);
        const c2 = a2 * x + b2 * y;
        o = opts(`${x},${y}`, () => `${y},${x}`, () => `${x + 1},${y}`, () => `${x},${y + 1}`);
        q = `方程组 ${a1}x + ${b1}y = ${c1} 与 ${a2}x + ${b2}y = ${c2} 的解是？`;
        exp = `代入检验：${a1}×${x} + ${b1}×${y} = ${c1}，${a2}×${x} + ${b2}×${y} = ${c2}，解为 x=${x}, y=${y}。`;
      } else if (type === 1) {
        // 加减消元
        const x = rnd(1, 6);
        const y = rnd(1, 6);
        const c1 = 2 * x + 3 * y;
        const c2 = 3 * x - 2 * y;
        o = opts(`${x},${y}`, () => `${y},${x}`, () => `${x + 1},${y}`, () => `${x},${y + 1}`);
        q = `方程组 2x + 3y = ${c1} 与 3x − 2y = ${c2} 的解是？`;
        exp = `加减消元：×2 + ×3 消 y，得 x = ${x}，代入得 y = ${y}。`;
      } else {
        // 应用题
        const a = rnd(1, 5), b = rnd(1, 5);
        const total = a + b;
        o = opts(`${a}个苹果`, () => `${b}个苹果`, () => `${total}个苹果`, () => `${Math.abs(a - b)}个苹果`);
        q = `买苹果和梨共 ${total} 个，苹果比梨多 ${a > b ? a - b : b - a} 个，苹果有几个？`;
        exp = `设苹果 x 个：x + (x − ${a > b ? a - b : b - a}) = ${total}，解得 x = ${a}。`;
      }
      results.push(Q(q, o, type < 2 ? "基础" : "进阶", exp, "二元一次方程组"));
    }
    return results;
  }

  /* ============================================================
   * 6. 线段与角（七年级）
   * ============================================================ */
  function qSegAngle(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 中点计算
        const a = rnd(2, 10) * 2;
        const mid = a / 2;
        o = opts(mid, () => mid + 1, () => mid - 1, () => a);
        q = `线段 AB = ${a}cm，M 是 AB 中点，AM = ？`;
        exp = `中点分线段为两等份，AM = AB ÷ 2 = ${a} ÷ 2 = ${mid}cm。`;
      } else if (type === 1) {
        // 角的度数
        const angle = rnd(30, 150);
        const supplement = 180 - angle;
        o = opts(supplement, () => 180 - supplement, () => 90 - angle, () => angle);
        q = `一个角为 ${angle}°，它的补角是？`;
        exp = `补角 = 180° − ${angle}° = ${supplement}°。`;
      } else {
        // 余角
        const angle = rnd(30, 60);
        const complement = 90 - angle;
        o = opts(complement, () => 90 - complement, () => 180 - angle, () => angle);
        q = `一个角为 ${angle}°，它的余角是？`;
        exp = `余角 = 90° − ${angle}° = ${complement}°。`;
      }
      results.push(Q(q, o, "基础", exp, "线段与角"));
    }
    return results;
  }

  /* ============================================================
   * 7. 三角形性质（七年级）
   * ============================================================ */
  function qTriangle(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 内角和
        const a = rnd(40, 80);
        const b = rnd(40, 80);
        const c = 180 - a - b;
        o = opts(c, () => a + b, () => 180 - a, () => 180 - b);
        q = `三角形两个角分别为 ${a}° 和 ${b}°，第三个角是？`;
        exp = `三角形内角和 = 180°，第三角 = 180° − ${a}° − ${b}° = ${c}°。`;
      } else if (type === 1) {
        // 外角定理
        const a = rnd(40, 70);
        const b = rnd(40, 70);
        const exterior = a + b;
        o = opts(exterior, () => 180 - exterior, () => a - b, () => a + b + 10);
        q = `三角形两个内角为 ${a}° 和 ${b}°，不相邻外角是？`;
        exp = `外角 = 两内角和 = ${a}° + ${b}° = ${exterior}°。`;
      } else {
        // 三边关系
        const a = rnd(3, 8);
        const b = rnd(3, 8);
        const c = rnd(Math.abs(a - b) + 1, a + b - 1);
        o = opts("能构成", () => "不能构成", () => "无法判断", () => "直角三角形");
        q = `三边长 ${a}, ${b}, ${c}，能否构成三角形？`;
        exp = `${a} + ${b} > ${c}，${a} + ${c} > ${b}，${b} + ${c} > ${a}，能构成三角形。`;
      }
      results.push(Q(q, o, "基础", exp, "三角形性质"));
    }
    return results;
  }

  /* ============================================================
   * 8. 全等三角形（八年级）
   * ============================================================ */
  function qCongruent(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 4;
      let q, ans, o, exp;
      if (type === 0) {
        // SAS判定
        o = opts("SAS", () => "ASA", () => "SSS", () => "AAS");
        q = `已知两边及其夹角对应相等，判定三角形全等的依据是？`;
        exp = `两边及其夹角对应相等 → SAS（边角边）全等判定。`;
      } else if (type === 1) {
        // ASA判定
        o = opts("ASA", () => "SAS", () => "SSS", () => "AAS");
        q = `已知两角及其夹边对应相等，判定三角形全等的依据是？`;
        exp = `两角及其夹边对应相等 → ASA（角边角）全等判定。`;
      } else if (type === 2) {
        // SSS判定
        o = opts("SSS", () => "SAS", () => "ASA", () => "AAS");
        q = `已知三边对应相等，判定三角形全等的依据是？`;
        exp = `三边对应相等 → SSS（边边边）全等判定。`;
      } else {
        // HL判定（直角三角形）
        o = opts("HL", () => "SAS", () => "ASA", () => "SSS");
        q = `直角三角形中，已知斜边和一条直角边对应相等，判定依据是？`;
        exp = `直角三角形特有的 HL（斜边、直角边）全等判定。`;
      }
      results.push(Q(q, o, "基础", exp, "全等三角形判定"));
    }
    return results;
  }

  /* ============================================================
   * 9. 相似三角形（八年级）
   * ============================================================ */
  function qSimilar(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 相似比计算
        const ratio = rnd(2, 5);
        const side1 = ratio * rnd(2, 5);
        const side2 = rnd(2, 5);
        o = opts(ratio + ":1", () => "1:" + ratio, () => (ratio + 1) + ":1", () => ratio + ":" + (ratio + 1));
        q = `两个相似三角形对应边分别为 ${side1}cm 和 ${side2}cm，相似比是？`;
        exp = `相似比 = ${side1} : ${side2} = ${ratio} : 1。`;
      } else if (type === 1) {
        // 面积比
        const ratio = rnd(2, 4);
        const area1 = ratio * ratio * rnd(1, 5);
        const area2 = rnd(1, 5);
        o = opts((ratio * ratio) + ":1", () => ratio + ":1", () => "1:" + (ratio * ratio), () => "1:1");
        q = `相似比为 ${ratio}:1 的两个三角形，面积比是？`;
        exp = `面积比 = 相似比的平方 = ${ratio}² : 1² = ${ratio * ratio} : 1。`;
      } else {
        // 平行线判定相似
        o = opts("平行线分线段成比例", () => "全等三角形", () => "勾股定理", () => "三角函数");
        q = `证明两个三角形相似，最常用的方法是？`;
        exp = `平行线截得的三角形与原三角形相似，利用平行线分线段成比例定理。`;
      }
      results.push(Q(q, o, "基础", exp, "相似三角形"));
    }
    return results;
  }

  /* ============================================================
   * 10. 勾股定理（八年级）
   * ============================================================ */
  function qPyth(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 已知两直角边求斜边（勾股数）
        const triples = [[3,4,5],[6,8,10],[5,12,13],[8,15,17],[9,12,15],[7,24,25]];
        const [a, b, c] = triples[i % triples.length];
        o = opts(c, () => a + b, () => Math.abs(a - b), () => a * b);
        q = `直角三角形两直角边为 ${a} 和 ${b}，斜边为？`;
        exp = `由勾股定理：c² = ${a}² + ${b}² = ${a*a} + ${b*b} = ${a*a + b*b}，c = ${c}。`;
      } else if (type === 1) {
        // 已知斜边和一直角边求另一直角边
        const triples = [[3,4,5],[6,8,10],[5,12,13],[8,15,17]];
        const [a, b, c] = triples[i % triples.length];
        o = opts(b, () => c - a, () => c + a, () => a * b / c);
        q = `直角三角形斜边 ${c}，一直角边 ${a}，另一直角边为？`;
        exp = `b² = c² − a² = ${c*c} − ${a*a} = ${c*c - a*a}，b = ${b}。`;
      } else {
        // 判断直角三角形
        const triples = [[3,4,5],[6,8,10],[5,12,13]];
        const [a, b, c] = triples[i % triples.length];
        o = opts("是直角三角形", () => "不是直角三角形", () => "无法判断", () => "等边三角形");
        q = `三边长为 ${a}, ${b}, ${c}，这个三角形是？`;
        exp = `${a}² + ${b}² = ${a*a} + ${b*b} = ${a*a + b*b} = ${c*c}，满足勾股定理，是直角三角形。`;
      }
      results.push(Q(q, o, "基础", exp, "勾股定理"));
    }
    return results;
  }

  /* ============================================================
   * 11. 四边形与平行四边形（八年级）
   * ============================================================ */
  function qQuad(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 4;
      let q, ans, o, exp;
      if (type === 0) {
        // 平行四边形性质
        o = opts("对边平行且相等", () => "对边不相等", () => "对角不相等", () => "四边相等");
        q = `平行四边形的性质是？`;
        exp = `平行四边形对边平行且相等，对角相等，邻角互补。`;
      } else if (type === 1) {
        // 矩形性质
        o = opts("对角线相等", () => "对角线不相等", () => "四边相等", () => "对角线垂直");
        q = `矩形的特有性质是？`;
        exp = `矩形对角线相等且互相平分，四个角都是直角。`;
      } else if (type === 2) {
        // 菱形性质
        o = opts("对角线互相垂直", () => "对角线相等", () => "四角相等", () => "对边不相等");
        q = `菱形的特有性质是？`;
        exp = `菱形对角线互相垂直且平分每组对角，四边相等。`;
      } else {
        // 正方形性质
        o = opts("对角线相等且垂直", () => "对角线不相等", () => "对角线不垂直", () => "四边不相等");
        q = `正方形的对角线性质是？`;
        exp = `正方形对角线相等、互相垂直且平分，每个对角线平分一组对角。`;
      }
      results.push(Q(q, o, "基础", exp, "四边形性质"));
    }
    return results;
  }

  /* ============================================================
   * 12. 圆的性质（九年级）
   * ============================================================ */
  function qCircle(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 4;
      let q, ans, o, exp;
      if (type === 0) {
        // 圆周角定理
        const central = rnd(60, 120);
        const inscribed = central / 2;
        o = opts(`${inscribed}°`, () => `${central}°`, () => `${90 - inscribed}°`, () => `${180 - central}°`);
        q = `圆心角为 ${central}°，同弧所对的圆周角是？`;
        exp = `圆周角 = 圆心角 ÷ 2 = ${central}° ÷ 2 = ${inscribed}°。`;
      } else if (type === 1) {
        // 圆的周长
        const r = rnd(2, 10);
        o = opts(`2${r}π`, () => `${r}π`, () => `${r*r}π`, () => `${4*r}π`);
        q = `半径为 ${r} 的圆，周长为？`;
        exp = `周长 C = 2πr = 2 × π × ${r} = 2${r}π。`;
      } else if (type === 2) {
        // 圆的面积
        const r = rnd(2, 10);
        o = opts(`${r*r}π`, () => `2${r}π`, () => `${r}π`, () => `${4*r}π`);
        q = `半径为 ${r} 的圆，面积为？`;
        exp = `面积 S = πr² = π × ${r}² = ${r*r}π。`;
      } else {
        // 弦与直径
        o = opts("直径", () => "弦", () => "切线", () => "弧");
        q = `圆中最长的弦是？`;
        exp = `直径是经过圆心的弦，是圆中最长的弦。`;
      }
      results.push(Q(q, o, "基础", exp, "圆的性质"));
    }
    return results;
  }

  /* ============================================================
   * 13. 一次函数（八年级）
   * ============================================================ */
  function qFunc1(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 4;
      let q, ans, o, exp;
      if (type === 0) {
        // 斜率计算
        const x1 = rnd(0, 5);
        const y1 = rnd(0, 5);
        const x2 = x1 + rnd(1, 5);
        const y2 = y1 + rnd(1, 5);
        const slope = (y2 - y1) / (x2 - x1);
        o = opts(slope, () => slope + 1, () => slope - 1, () => (y1 - y2) / (x1 - x2));
        q = `点 (${x1},${y1}) 和 (${x2},${y2}) 连线的斜率是？`;
        exp = `斜率 k = (y₂−y₁)/(x₂−x₁) = (${y2}−${y1})/(${x2}−${x1}) = ${slope}。`;
      } else if (type === 1) {
        // 截距
        const k = rnd(1, 3);
        const b = rnd(-5, 5);
        o = opts(b, () => k, () => 0, () => -b);
        q = `一次函数 y = ${k}x + ${b}，y 轴截距是？`;
        exp = `y 轴截距是 x=0 时的 y 值，即 b = ${b}。`;
      } else if (type === 2) {
        // 函数值
        const k = rnd(1, 3);
        const b = rnd(1, 5);
        const x = rnd(1, 5);
        const y = k * x + b;
        o = opts(y, () => k + b, () => x * b, () => k * b);
        q = `一次函数 y = ${k}x + ${b}，当 x = ${x} 时，y = ？`;
        exp = `y = ${k}×${x} + ${b} = ${y}。`;
      } else {
        // 图像性质
        const k = rnd(1, 3);
        o = opts("上升", () => "下降", () => "水平", () => "垂直");
        q = `一次函数 y = ${k}x + 1，图像从左到右？`;
        exp = `k = ${k} > 0，图像从左向右上升。`;
      }
      results.push(Q(q, o, type < 3 ? "基础" : "进阶", exp, "一次函数"));
    }
    return results;
  }

  /* ============================================================
   * 14. 反比例函数（八年级）
   * ============================================================ */
  function qInverse(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 3;
      let q, ans, o, exp;
      if (type === 0) {
        // 求 k 值
        const k = rnd(2, 12);
        const x = rnd(1, 5);
        const y = k / x;
        o = opts(k, () => k * 2, () => k / 2, () => x + y);
        q = `反比例函数 y = k/x 经过点 (${x},${y})，k 的值为？`;
        exp = `k = x × y = ${x} × ${y} = ${k}。`;
      } else if (type === 1) {
        // 图像位置
        const k = rnd(1, 5);
        o = opts("一、三象限", () => "二、四象限", () => "一、二象限", () => "三、四象限");
        q = `反比例函数 y = ${k}/x，图像在？`;
        exp = `k = ${k} > 0，图像在第一、三象限。`;
      } else {
        // 函数值
        const k = rnd(2, 10);
        const x = rnd(1, 5);
        const y = k / x;
        o = opts(y, () => k + x, () => k - x, () => x / k);
        q = `反比例函数 y = ${k}/x，当 x = ${x} 时，y = ？`;
        exp = `y = ${k} ÷ ${x} = ${y}。`;
      }
      results.push(Q(q, o, "基础", exp, "反比例函数"));
    }
    return results;
  }

  /* ============================================================
   * 15. 二次函数（九年级）
   * ============================================================ */
  function qQuadfunc(n) {
    const results = [];
    for (let i = 0; i < n; i++) {
      const type = i % 5;
      let q, ans, o, exp;
      if (type === 0) {
        // 顶点坐标
        const h = rnd(-3, 3);
        const k = rnd(-3, 3);
        o = opts(`(${h},${k})`, () => `(${-h},${k})`, () => `(${h},${-k})`, () => `(${-h},${-k})`);
        q = `二次函数 y = (x − ${h})² + ${k} 的顶点坐标是？`;
        exp = `顶点式为 y = a(x−h)² + k，顶点为 (${h},${k})。`;
      } else if (type === 1) {
        // 开口方向
        const a = rnd(1, 5) * (Math.random() < 0.5 ? 1 : -1);
        o = opts(a > 0 ? "开口向上" : "开口向下", () => a > 0 ? "开口向下" : "开口向上", () => "无法判断", () => "开口水平");
        q = `二次函数 y = ${a}x² + 2x + 1，开口方向？`;
        exp = `a = ${a} ${a > 0 ? ">" : "<"} 0，开口${a > 0 ? "向上" : "向下"}。`;
      } else if (type === 2) {
        // 对称轴
        const h = rnd(-3, 3);
        o = opts(`x = ${h}`, () => `x = ${-h}`, () => `y = ${h}`, () => `y = ${-h}`);
        q = `二次函数 y = (x + ${h > 0 ? -h : h})² 的对称轴是？`;
        exp = `对称轴为 x = ${h}。`;
      } else if (type === 3) {
        // 与 y 轴交点
        const c = rnd(-5, 5);
        o = opts(`(0,${c})`, () => `(${c},0)`, () => `(0,0)`, () => `(1,${c})`);
        q = `二次函数 y = x² + 2x + ${c}，与 y 轴交点是？`;
        exp = `令 x = 0，y = ${c}，交点为 (0, ${c})。`;
      } else {
        // 最值
        const a = -Math.abs(rnd(1, 3));
        const k = rnd(1, 5);
        o = opts(`最大值 ${k}`, () => `最小值 ${k}`, () => `最大值 ${-k}`, () => `无最值`);
        q = `二次函数 y = ${a}x² + 2x + ${k + 1}，有最值吗？`;
        exp = `a = ${a} < 0，开口向下，有最大值 ${k}。`;
      }
      results.push(Q(q, o, "基础", exp, "二次函数"));
    }
    return results;
  }

  /* ============================================================
   * 注册到 window.TECHNIQUES
   * ============================================================ */
  const GEN = {
    rational: qRational,
    integral: qIntegral,
    linear1: qLinear,
    inequal: qInequal,
    system: qSystem,
    segangle: qSegAngle,
    triangle: qTriangle,
    congruent: qCongruent,
    similar: qSimilar,
    pyth: qPyth,
    quad: qQuad,
    circ: qCircle,
    func1: qFunc1,
    inverse: qInverse,
    quadfunc: qQuadfunc
  };

  if (window.TECHNIQUES) {
    window.TECHNIQUES.forEach(t => {
      if (GEN[t.id]) t.qgen = GEN[t.id];
    });
  }
  window.QGEN_JUNIOR_READY = true;
})();
