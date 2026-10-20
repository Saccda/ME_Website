"""Mathematics templates, one family per domain and difficulty.

Every template declares the computation it is built from, so `validate` can
recompute the answer and refuse the question if the key disagrees. That is what
makes these machine-provable rather than author-asserted.

Topics follow Part One, Revision of Mathematics, of Bird & Ross. The numbers,
wording and distractors are generated here; no question is taken from any book.
"""
import math


def fmt(value, digits=2):
    # Only trailing zeros *after a decimal point* are noise. Stripping them
    # unconditionally turned 200000 into "2" whenever digits was 0, because the
    # integer's own zeros were trailing characters too. The existing digits=0
    # caller escaped it only because no power of two ends in a zero.
    text = f"{round(value, digits):.{digits}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def vec(c):
    """A 3-vector as "2i - 3j + 4k", written the way it is written by hand.

    A zero component is left out and a unit one loses its 1, which is correct
    notation but means the string cannot be parsed back for a number -- "i - 7j"
    leads with 7, not 1. So this is for reading only: anything a validator has
    to recompute is asked for as a single component instead.
    """
    parts = []
    for value, letter in zip(c, "ijk"):
        if value == 0:
            continue
        size = "" if abs(value) == 1 else str(abs(value))
        term = f"{size}{letter}"
        if not parts:
            parts.append(f"-{term}" if value < 0 else term)
        else:
            parts.append(f"{'-' if value < 0 else '+'} {term}")
    return " ".join(parts) if parts else "0"


def build(value, unit, variants, digits=2):
    """Correct option plus distractors, each a distinct number.

    For some parameter draws two of a template's error models land on the same
    number and one is dropped. The slips below top the list back up, so a
    five-option question is always possible; they are only reached when the
    template's own distractors run short.
    """
    fallbacks = [
        (value * 10, "A slip of one power of ten.", "scale-error"),
        (value / 10, "A slip of one power of ten.", "scale-error"),
        (value * 2, "The result is doubled.", "scale-error"),
        (value / 2, "The result is halved.", "scale-error"),
        (-value, "The sign is reversed.", "sign-error"),
        # Additive, so they stay distinct even when the answer is zero and every
        # multiplicative slip above collapses onto it.
        (value + 1, "An arithmetic slip of one unit.", "arithmetic-slip"),
        (value - 1, "An arithmetic slip of one unit.", "arithmetic-slip"),
    ]
    correct = f"{fmt(value, digits)}{unit}"
    seen = {fmt(value, digits)}
    wrong = []
    for other, why, tag in list(variants) + fallbacks:
        if len(wrong) >= 5:
            break
        key = fmt(other, digits)
        if key in seen or other != other or abs(other) > 1e9:
            continue
        # A distractor that rounds away to zero is eliminated on sight -- no
        # resistance, no energy, no charge -- so it wastes an option instead of
        # testing anything. Only an answer that is itself zero may be zero.
        if key == "0" and fmt(value, digits) != "0":
            continue
        seen.add(key)
        wrong.append((f"{key}{unit}", why, tag))
    return correct, wrong


def template(domain, depth, rng):
    """Return stem, answer, explanation, distractors, validator spec and LaTeX."""
    if domain == "number":
        if depth == 0:
            a, b, n = rng.randint(2, 5), rng.choice([8, 10, 16, 20]), rng.choice([120, 160, 200, 240])
            value = n * a / b
            stem = f"What is ${a}/{b}$ of {n}?"
            spec = {"kind": "compute", "vars": {"n": n, "a": a, "b": b}, "expr": "n*a/b", "digits": 2}
            explain = f"Multiply by the numerator and divide by the denominator: ${n} \\times {a} \\div {b} = {fmt(value)}$."
            latex = rf"\frac{{{a}}}{{{b}}} \times {n} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (n * b / a, "Inverts the fraction.", "inverted-operation"),
                (n * a, "Forgets to divide by the denominator.", "missing-step"),
                (n / b, "Forgets the numerator.", "missing-step"),
                (n - a * b, "Subtracts instead of taking a fraction.", "wrong-operation")])
        elif depth == 1:
            p, cost = rng.choice([8, 12, 15, 20, 25]), rng.choice([250, 320, 480, 640])
            value = cost * (1 + p / 100)
            stem = f"A component costs {cost} units. The price rises by {p}%. What is the new price?"
            spec = {"kind": "compute", "vars": {"c": cost, "p": p}, "expr": "c*(1+p/100)", "digits": 2}
            explain = f"A {p}% rise multiplies the price by ${1 + p / 100}$, giving {fmt(value)}."
            latex = rf"{cost} \times \left(1 + \frac{{{p}}}{{100}}\right) = {fmt(value)}"
            correct, wrong = build(value, "", [
                (cost * (1 - p / 100), "Applies the change as a decrease.", "sign-error"),
                (cost + p, "Adds the percentage as a plain number.", "percent-as-number"),
                (cost * p / 100, "Gives only the increase, not the new price.", "partial-answer"),
                (cost * (1 + p), "Treats the percentage as a whole multiple.", "scale-error")])
        elif depth == 2:
            a, b, teeth = rng.randint(2, 5), rng.randint(6, 11), rng.choice([24, 36, 48, 60])
            value = teeth * b / a
            stem = f"Two gears are in the ratio {a}:{b}. The first has {teeth} teeth. How many teeth has the second?"
            spec = {"kind": "compute", "vars": {"t": teeth, "a": a, "b": b}, "expr": "t*b/a", "digits": 2}
            explain = f"Scale by the ratio: ${teeth} \\times {b} \\div {a} = {fmt(value)}$."
            latex = rf"{teeth} \times \frac{{{b}}}{{{a}}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (teeth * a / b, "Uses the ratio the wrong way round.", "inverted-ratio"),
                (teeth + b - a, "Adds the difference instead of scaling.", "wrong-operation"),
                (teeth * b, "Omits the first part of the ratio.", "missing-step"),
                (teeth * b / (a + b), "Divides by the total of the ratio instead of the first part.", "wrong-base")])
        else:
            before, after = rng.choice([80, 120, 150, 200]), None
            after = before - rng.choice([12, 18, 24, 30])
            value = (before - after) / before * 100
            stem = f"A reading falls from {before} to {after}. What is the percentage decrease?"
            spec = {"kind": "compute", "vars": {"a": before, "b": after}, "expr": "(a-b)/a*100", "digits": 2}
            explain = f"Divide the fall by the original value: $({before}-{after})/{before} \\times 100 = {fmt(value)}\\%$."
            latex = rf"\frac{{{before}-{after}}}{{{before}}} \times 100 = {fmt(value)}"
            correct, wrong = build(value, "%", [
                ((before - after) / after * 100, "Divides by the new value, not the original.", "wrong-base"),
                (before - after, "Gives the fall itself, not a percentage.", "partial-answer"),
                (after / before * 100, "Gives what remains, not the decrease.", "complement-error"),
                ((before - after) / before, "Omits the factor of 100.", "scale-error")])

    elif domain == "algebra":
        if depth == 0:
            a, b, c, d, x = rng.randint(2, 6), rng.randint(2, 9), rng.randint(2, 5), rng.randint(2, 7), rng.randint(2, 6)
            value = a * (x + b) - c * (x - d)
            stem = f"If $x = {x}$, evaluate ${a}(x + {b}) - {c}(x - {d})$."
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c, "d": d, "x": x}, "expr": "a*(x+b)-c*(x-d)", "digits": 2}
            explain = f"Expand both brackets, then substitute $x={x}$: ${a}({x}+{b}) - {c}({x}-{d}) = {fmt(value)}$."
            latex = rf"{a}({x}+{b}) - {c}({x}-{d}) = {fmt(value)}"
            correct, wrong = build(value, "", [
                (a * (x + b) + c * (x - d), "Keeps the sign of the second bracket.", "sign-error"),
                (a * x + b - c * x - d, "Multiplies only the first term in each bracket.", "partial-expansion"),
                (a * (x + b) - c * x - d, "Does not distribute over the second bracket.", "partial-expansion"),
                ((a - c) * x, "Drops the constant terms.", "missing-step")])
        elif depth == 1:
            a, b, c = rng.randint(3, 7), rng.randint(2, 6), rng.randint(1, 4)
            value = 2 ** (a + b - c)
            stem = f"Simplify $\\frac{{2^{{{a}}} \\times 2^{{{b}}}}}{{2^{{{c}}}}}$ and give its value."
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c}, "expr": "2**(a+b-c)", "digits": 0}
            explain = f"Add the indices when multiplying and subtract when dividing: $2^{{{a}+{b}-{c}}} = 2^{{{a + b - c}}} = {value:g}$."
            latex = rf"2^{{{a}+{b}-{c}}} = 2^{{{a + b - c}}}"
            correct, wrong = build(value, "", [
                (2 ** (a + b + c), "Adds the index that should be subtracted.", "sign-error"),
                (2 ** (a * b - c), "Multiplies the indices instead of adding.", "index-law-error"),
                (a + b - c, "Gives the index rather than its value.", "partial-answer"),
                (2 ** (a + b) - c, "Subtracts the number instead of the index.", "index-law-error")], digits=0)
        elif depth == 2:
            a, b, c = rng.randint(3, 9), rng.randint(2, 14), rng.randint(20, 70)
            value = (c - b) / a
            stem = f"Solve ${a}x + {b} = {c}$ for $x$."
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c}, "expr": "(c-b)/a", "digits": 2}
            explain = f"Subtract {b} from both sides, then divide by {a}: $x = ({c}-{b})/{a} = {fmt(value)}$."
            latex = rf"x = \frac{{{c}-{b}}}{{{a}}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                ((c + b) / a, "Adds the constant instead of subtracting it.", "sign-error"),
                (c / a - b, "Divides before moving the constant.", "order-of-operations"),
                (c - b, "Does not divide by the coefficient.", "missing-step"),
                (a / (c - b), "Inverts the final division.", "inverted-operation")])
        else:
            a, b, c, d = rng.randint(2, 5), rng.randint(1, 4), rng.randint(1, 4), rng.randint(2, 5)
            x0, y0 = rng.randint(2, 6), rng.randint(2, 6)
            e, f = a * x0 + b * y0, c * x0 + d * y0
            if a * d - b * c == 0:
                d += 1
                f = c * x0 + d * y0
            value = (e * d - b * f) / (a * d - b * c)
            stem = (f"Solve the simultaneous equations ${a}x + {b}y = {e}$ and "
                    f"${c}x + {d}y = {f}$ for $x$.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f},
                    "expr": "(e*d - b*f)/(a*d - b*c)", "digits": 2}
            explain = (f"Eliminate $y$ by scaling: $x = (({e})({d}) - ({b})({f})) / (({a})({d}) - ({b})({c})) "
                       f"= {fmt(value)}$.")
            latex = rf"x = \frac{{{e} \times {d} - {b} \times {f}}}{{{a} \times {d} - {b} \times {c}}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                ((f * d - b * e) / (a * d - b * c), "Swaps the two constants.", "substitution-error"),
                ((e * d + b * f) / (a * d - b * c), "Adds where the elimination subtracts.", "sign-error"),
                ((e * d - b * f) / (a * d + b * c), "Adds in the denominator.", "sign-error"),
                (y0, "Solves for the other unknown.", "wrong-variable")])

    elif domain == "triangles":
        if depth == 0:
            deg = rng.choice([30, 45, 60, 75, 120, 135])
            value = deg * math.pi / 180
            stem = f"Convert ${deg}^\\circ$ to radians, correct to 3 decimal places."
            spec = {"kind": "compute", "vars": {"d": deg}, "expr": "d*pi/180", "digits": 3}
            explain = f"Multiply by $\\pi/180$: ${deg} \\times \\pi \\div 180 = {fmt(value, 3)}$ rad."
            latex = rf"{deg} \times \frac{{\pi}}{{180}} = {fmt(value, 3)}"
            correct, wrong = build(value, " rad", [
                (deg * 180 / math.pi, "Converts the wrong way.", "inverted-conversion"),
                (deg / 180, "Leaves out $\\pi$.", "missing-step"),
                (deg * math.pi, "Leaves out the division by 180.", "missing-step"),
                (deg / math.pi, "Divides by $\\pi$ instead of multiplying.", "inverted-operation")], digits=3)
        elif depth == 1:
            opp, hyp = rng.randint(3, 9), rng.randint(11, 18)
            value = math.degrees(math.asin(opp / hyp))
            stem = (f"In a right-angled triangle the side opposite angle $\\theta$ is {opp} and the "
                    f"hypotenuse is {hyp}. Find $\\theta$ in degrees, to 2 decimal places.")
            spec = {"kind": "compute", "vars": {"o": opp, "h": hyp}, "expr": "degrees(asin(o/h))", "digits": 2}
            explain = f"$\\sin\\theta = {opp}/{hyp}$, so $\\theta = \\sin^{{-1}}({fmt(opp / hyp, 4)}) = {fmt(value)}^\\circ$."
            latex = rf"\theta = \sin^{{-1}}\left(\frac{{{opp}}}{{{hyp}}}\right) = {fmt(value)}"
            correct, wrong = build(value, "°", [
                (math.degrees(math.acos(opp / hyp)), "Uses cosine instead of sine.", "wrong-ratio"),
                (math.degrees(math.atan(opp / hyp)), "Uses tangent instead of sine.", "wrong-ratio"),
                (math.asin(opp / hyp), "Leaves the answer in radians.", "unit-error"),
                (opp / hyp * 100, "Reports the ratio, not the angle.", "partial-answer")])
        elif depth == 2:
            a, b = rng.randint(3, 12), rng.randint(4, 15)
            value = math.sqrt(a ** 2 + b ** 2)
            stem = f"A right-angled triangle has shorter sides {a} and {b}. Find the hypotenuse, to 2 decimal places."
            spec = {"kind": "compute", "vars": {"a": a, "b": b}, "expr": "sqrt(a**2+b**2)", "digits": 2}
            explain = f"By Pythagoras, $c = \\sqrt{{{a}^2 + {b}^2}} = {fmt(value)}$."
            latex = rf"c = \sqrt{{{a}^2 + {b}^2}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (a + b, "Adds the sides instead of using Pythagoras.", "wrong-operation"),
                (math.sqrt(abs(a ** 2 - b ** 2)), "Subtracts the squares.", "sign-error"),
                (a ** 2 + b ** 2, "Omits the square root.", "missing-step"),
                (math.sqrt(a + b), "Takes the root of the sum of the sides.", "missing-step")])
        else:
            a, b, angle = rng.randint(5, 12), rng.randint(6, 14), rng.choice([40, 55, 70, 100, 115])
            value = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(angle)))
            stem = (f"Two sides of a triangle are {a} and {b}, with an included angle of {angle}°. "
                    f"Find the third side, to 2 decimal places.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "C": angle},
                    "expr": "sqrt(a**2+b**2-2*a*b*cos(radians(C)))", "digits": 2}
            explain = (f"By the cosine rule, $c^2 = {a}^2 + {b}^2 - 2({a})({b})\\cos {angle}^\\circ$, "
                       f"so $c = {fmt(value)}$.")
            latex = rf"c = \sqrt{{{a}^2 + {b}^2 - 2 \times {a} \times {b} \cos {angle}^\circ}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (math.sqrt(a ** 2 + b ** 2 + 2 * a * b * math.cos(math.radians(angle))), "Adds the cosine term.", "sign-error"),
                (math.sqrt(a ** 2 + b ** 2), "Ignores the included angle.", "missing-step"),
                (math.sqrt(abs(a ** 2 + b ** 2 - 2 * a * b * math.cos(angle))), "Uses the angle in radians.", "unit-error"),
                (a + b, "Adds the two sides.", "wrong-operation")])

    elif domain == "units":
        if depth == 0:
            metres = rng.choice([1.5, 2.4, 3.6, 0.85, 12.5])
            value = metres * 1000
            stem = f"How many millimetres are there in {metres} metres?"
            spec = {"kind": "compute", "vars": {"m": metres}, "expr": "m*1000", "digits": 2}
            explain = f"One metre is 1000 mm, so ${metres} \\times 1000 = {fmt(value)}$ mm."
            latex = rf"{metres} \times 10^3 = {fmt(value)}"
            correct, wrong = build(value, " mm", [
                (metres * 100, "Converts to centimetres.", "prefix-error"),
                (metres / 1000, "Divides instead of multiplying.", "inverted-conversion"),
                (metres * 10, "Uses the wrong power of ten.", "prefix-error"),
                (metres * 1000000, "Converts to micrometres.", "prefix-error")])
        elif depth == 1:
            kn = rng.choice([2.5, 4.8, 7.2, 15.6])
            value = kn * 1000
            stem = f"A force of {kn} kN expressed in newtons is:"
            spec = {"kind": "compute", "vars": {"k": kn}, "expr": "k*1000", "digits": 2}
            explain = f"The prefix kilo means $10^3$, so ${kn}\\,\\text{{kN}} = {fmt(value)}\\,\\text{{N}}$."
            latex = rf"{kn} \times 10^3\ \text{{N}} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (kn / 1000, "Treats kilo as a division.", "inverted-conversion"),
                (kn * 100, "Uses $10^2$ for kilo.", "prefix-error"),
                (kn * 10 ** 6, "Uses the prefix for mega.", "prefix-error"),
                (kn, "Leaves the value unchanged.", "missing-step")])
        elif depth == 2:
            kph = rng.choice([36, 54, 72, 90, 108])
            value = kph * 1000 / 3600
            stem = f"Convert {kph} km/h to m/s, correct to 2 decimal places."
            spec = {"kind": "compute", "vars": {"s": kph}, "expr": "s*1000/3600", "digits": 2}
            explain = f"Multiply by 1000 and divide by 3600: ${kph} \\times 1000 \\div 3600 = {fmt(value)}$ m/s."
            latex = rf"\frac{{{kph} \times 1000}}{{3600}} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (kph * 3600 / 1000, "Converts m/s to km/h instead.", "inverted-conversion"),
                (kph / 3600, "Divides by the seconds but forgets to convert kilometres.", "missing-step"),
                (kph / 60, "Divides by minutes only.", "missing-step"),
                (kph * 1000 / 60, "Uses minutes instead of seconds.", "unit-error")])
        else:
            density = rng.choice([2.7, 7.8, 8.9, 1.2])
            value = density * 1000
            stem = f"A material has a density of {density} g/cm³. Express this in kg/m³."
            spec = {"kind": "compute", "vars": {"d": density}, "expr": "d*1000", "digits": 2}
            explain = (f"$1\\,\\text{{g/cm}}^3 = 1000\\,\\text{{kg/m}}^3$, because the gram is $10^{{-3}}$ kg and "
                       f"the cubic centimetre is $10^{{-6}}$ m³. So the answer is {fmt(value)} kg/m³.")
            latex = rf"{density}\ \text{{g/cm}}^3 = {fmt(value)}\ \text{{kg/m}}^3"
            correct, wrong = build(value, " kg/m³", [
                (density / 1000, "Divides instead of multiplying.", "inverted-conversion"),
                (density * 100, "Uses only two powers of ten.", "prefix-error"),
                (density * 10 ** 6, "Applies the cubic factor twice.", "prefix-error"),
                (density, "Leaves the value unchanged.", "missing-step")])

    elif domain == "graphs":
        if depth == 0:
            m, c, x = rng.randint(2, 7), rng.randint(-8, 9), rng.randint(2, 9)
            value = m * x + c
            stem = f"A straight line has equation $y = {m}x + ({c})$. Find $y$ when $x = {x}$."
            spec = {"kind": "compute", "vars": {"m": m, "c": c, "x": x}, "expr": "m*x+c", "digits": 2}
            explain = f"Substitute $x = {x}$: $y = {m}({x}) + ({c}) = {fmt(value)}$."
            latex = rf"y = {m} \times {x} + ({c}) = {fmt(value)}"
            correct, wrong = build(value, "", [
                (m * x - c, "Subtracts the intercept.", "sign-error"),
                (m + x + c, "Adds the gradient instead of multiplying.", "wrong-operation"),
                (m * (x + c), "Multiplies the intercept by the gradient.", "order-of-operations"),
                (x + c, "Omits the gradient.", "missing-step")])
        elif depth == 1:
            x1, y1 = rng.randint(1, 5), rng.randint(1, 9)
            x2, y2 = x1 + rng.randint(2, 6), y1 + rng.randint(3, 14)
            value = (y2 - y1) / (x2 - x1)
            stem = f"Find the gradient of the line through $({x1}, {y1})$ and $({x2}, {y2})$."
            spec = {"kind": "compute", "vars": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                    "expr": "(y2-y1)/(x2-x1)", "digits": 2}
            explain = f"Gradient is the change in $y$ over the change in $x$: $({y2}-{y1})/({x2}-{x1}) = {fmt(value)}$."
            latex = rf"m = \frac{{{y2}-{y1}}}{{{x2}-{x1}}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                ((x2 - x1) / (y2 - y1), "Inverts the gradient.", "inverted-operation"),
                (y2 - y1, "Uses the rise without the run.", "missing-step"),
                ((y2 + y1) / (x2 + x1), "Adds the coordinates instead of subtracting.", "sign-error"),
                ((y2 - y1) / (x2 + x1), "Adds in the denominator.", "sign-error")])
        elif depth == 2:
            m, x1, y1 = rng.randint(2, 6), rng.randint(2, 7), rng.randint(5, 20)
            if y1 == m * x1:  # a zero intercept makes a dull question
                y1 += 3
            value = y1 - m * x1
            stem = f"A line of gradient {m} passes through $({x1}, {y1})$. Find its $y$-intercept."
            spec = {"kind": "compute", "vars": {"m": m, "x1": x1, "y1": y1}, "expr": "y1-m*x1", "digits": 2}
            explain = f"From $y = mx + c$, $c = {y1} - {m}({x1}) = {fmt(value)}$."
            latex = rf"c = {y1} - {m} \times {x1} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (y1 + m * x1, "Adds instead of subtracting.", "sign-error"),
                (m * x1 - y1, "Reverses the subtraction.", "sign-error"),
                (y1 / m - x1, "Divides by the gradient.", "wrong-operation"),
                (y1 - x1, "Omits the gradient.", "missing-step")])
        elif rng.random() < 0.45:
            # The paper plots resistance against voltage and asks for the line's
            # equation, and elsewhere draws four lines and asks which one a given
            # equation belongs to. Both are the same work -- gradient and
            # intercept -- and both can be set from two readings instead of a
            # drawing, which a generated question cannot supply.
            x1, y1 = rng.randint(0, 3), rng.choice([10, 20, 40])
            x2 = x1 + rng.choice([4, 5, 8, 10])
            slope = rng.choice([0.8, 1.25, 1.45, 2.5])
            y2 = y1 + slope * (x2 - x1)
            # Asked at a third point, so the answer is a number the server can
            # recompute rather than an equation it would have to parse.
            x = x2 + rng.choice([2, 4, 6])
            value = slope * x + y1 - slope * x1
            stem = (f"A resistance-against-voltage plot is a straight line through "
                    f"$({x1}, {y1})$ and $({x2}, {fmt(y2)})$, with resistance in ohms and "
                    f"voltage in volts. What resistance does it give at ${x}$ V, to 2 decimal "
                    f"places?")
            spec = {"kind": "compute",
                    "vars": {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x": x},
                    "expr": "(y2-y1)/(x2-x1)*(x-x1)+y1", "digits": 2}
            intercept = y1 - slope * x1
            explain = (f"The gradient is $\\frac{{{fmt(y2)} - {y1}}}{{{x2} - {x1}}} = "
                       f"{fmt(slope)}$ Ω per volt and the intercept is {fmt(intercept)} Ω, so the "
                       f"line is $R = {fmt(slope)}V + {fmt(intercept)}$. At {x} V that gives "
                       f"{fmt(value)} Ω.")
            latex = rf"R = {fmt(slope)}V + {fmt(intercept)} = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (slope * x, "Uses the gradient but drops the intercept.", "missing-step"),
                (intercept, "Reports the intercept, which is the value at zero volts.", "partial-answer"),
                (slope * (x - x1) + y1 + slope, "Reads one step too far along the line.", "extra-step"),
                (y2, "Repeats the second reading.", "partial-answer")])
        else:
            x1, y1 = rng.randint(1, 4), rng.randint(2, 8)
            x2, y2 = x1 + rng.randint(3, 6), y1 + rng.randint(6, 18)
            x = x2 + rng.randint(2, 5)
            slope = (y2 - y1) / (x2 - x1)
            value = slope * x + (y1 - slope * x1)
            stem = (f"A test gives readings $({x1}, {y1})$ and $({x2}, {y2})$ on a straight line. "
                    f"Predict the reading at $x = {x}$, to 2 decimal places.")
            spec = {"kind": "compute", "vars": {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x": x},
                    "expr": "(y2-y1)/(x2-x1)*x + (y1 - (y2-y1)/(x2-x1)*x1)", "digits": 2}
            explain = (f"The gradient is {fmt(slope)}, and the intercept is {fmt(y1 - slope * x1)}, "
                       f"so at $x = {x}$ the reading is {fmt(value)}.")
            latex = rf"y = {fmt(slope)} \times {x} + ({fmt(y1 - slope * x1)}) = {fmt(value)}"
            correct, wrong = build(value, "", [
                (slope * x, "Omits the intercept.", "missing-step"),
                (y2 + slope, "Adds one gradient to the last reading.", "wrong-operation"),
                (slope * x - (y1 - slope * x1), "Subtracts the intercept.", "sign-error"),
                (y2, "Repeats the last reading.", "partial-answer")])

    elif domain == "calculus":
        if depth == 0:
            a, n, x = rng.randint(2, 7), rng.randint(2, 4), rng.randint(2, 5)
            value = a * n * x ** (n - 1)
            stem = f"If $y = {a}x^{{{n}}}$, find $\\frac{{dy}}{{dx}}$ when $x = {x}$."
            spec = {"kind": "compute", "vars": {"a": a, "n": n, "x": x}, "expr": "a*n*x**(n-1)", "digits": 2}
            explain = f"Differentiating gives $\\frac{{dy}}{{dx}} = {a * n}x^{{{n - 1}}}$, which at $x={x}$ is {fmt(value)}."
            latex = rf"\frac{{dy}}{{dx}} = {a * n}x^{{{n - 1}}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (a * x ** n, "Substitutes without differentiating.", "missing-step"),
                (a * n * x ** n, "Does not reduce the index.", "index-law-error"),
                (a * (n - 1) * x ** (n - 1), "Uses the reduced index as the multiplier.", "index-law-error"),
                (n * x ** (n - 1), "Drops the coefficient.", "missing-step")])
        elif depth == 1:
            a, b, t = rng.randint(2, 6), rng.randint(3, 11), rng.randint(2, 6)
            value = 2 * a * t + b
            stem = (f"A body moves so that $s = {a}t^2 + {b}t$ metres. Find its velocity at $t = {t}$ s.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "t": t}, "expr": "2*a*t+b", "digits": 2}
            explain = f"Velocity is $\\frac{{ds}}{{dt}} = {2 * a}t + {b}$, so at $t={t}$ it is {fmt(value)} m/s."
            latex = rf"v = {2 * a}t + {b} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (a * t ** 2 + b * t, "Gives the displacement, not the velocity.", "missing-step"),
                (2 * a * t, "Drops the constant term after differentiating.", "missing-step"),
                (a * t + b, "Does not bring down the index.", "index-law-error"),
                (2 * a, "Gives the acceleration.", "wrong-quantity")])
        elif depth == 2:
            a, n, u = rng.randint(2, 6), rng.randint(1, 3), rng.randint(2, 4)
            value = a * u ** (n + 1) / (n + 1)
            stem = f"Evaluate $\\int_0^{{{u}}} {a}x^{{{n}}}\\,dx$."
            spec = {"kind": "compute", "vars": {"a": a, "n": n, "u": u}, "expr": "a*u**(n+1)/(n+1)", "digits": 2}
            explain = (f"Integrating gives $\\frac{{{a}x^{{{n + 1}}}}}{{{n + 1}}}$; at $x={u}$ this is {fmt(value)} "
                       f"and at $x=0$ it is 0.")
            latex = rf"\int_0^{{{u}}} {a}x^{{{n}}}\,dx = \frac{{{a} \times {u}^{{{n + 1}}}}}{{{n + 1}}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (a * u ** n, "Does not raise the index or divide.", "missing-step"),
                (a * n * u ** (n - 1), "Differentiates instead of integrating.", "wrong-operation"),
                (a * u ** (n + 1), "Raises the index but omits the division.", "missing-step"),
                (a * u ** (n + 1) / n, "Divides by the original index.", "index-law-error")])
        else:
            a, b = rng.randint(2, 6), rng.randint(1, 8)
            low, up = rng.randint(1, 3), rng.randint(4, 7)
            value = a * (up ** 2 - low ** 2) / 2 + b * (up - low)
            stem = f"Evaluate $\\int_{{{low}}}^{{{up}}} ({a}x + {b})\\,dx$."
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "l": low, "u": up},
                    "expr": "a*(u**2-l**2)/2 + b*(u-l)", "digits": 2}
            explain = (f"The integral is $\\frac{{{a}x^2}}{{2}} + {b}x$. Evaluating between {low} and {up} "
                       f"gives {fmt(value)}.")
            latex = rf"\left[\frac{{{a}x^2}}{{2}} + {b}x\right]_{{{low}}}^{{{up}}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (a * (up ** 2 - low ** 2) / 2, "Omits the constant term.", "missing-step"),
                (a * (up ** 2 + low ** 2) / 2 + b * (up + low), "Adds the limits instead of subtracting.", "sign-error"),
                (a * up ** 2 / 2 + b * up, "Uses the upper limit only.", "missing-step"),
                (a * (up - low) + b, "Does not integrate the first term.", "wrong-operation")])

    elif domain == "vectors":
        if depth == 0:
            force, angle = rng.choice([40, 60, 80, 120]), rng.choice([25, 35, 50, 65])
            value = force * math.cos(math.radians(angle))
            stem = (f"A force of {force} N acts at {angle}° to the horizontal. Find its horizontal "
                    f"component, to 2 decimal places.")
            spec = {"kind": "compute", "vars": {"f": force, "t": angle}, "expr": "f*cos(radians(t))", "digits": 2}
            explain = f"The horizontal component is $F\\cos\\theta = {force}\\cos {angle}^\\circ = {fmt(value)}$ N."
            latex = rf"F_x = {force}\cos {angle}^\circ = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (force * math.sin(math.radians(angle)), "Uses sine, which gives the vertical component.", "wrong-ratio"),
                (force * math.tan(math.radians(angle)), "Uses tangent.", "wrong-ratio"),
                (force * math.cos(angle), "Uses the angle in radians.", "unit-error"),
                (force / math.cos(math.radians(angle)), "Divides by the cosine.", "inverted-operation")])
        elif depth == 1:
            a, b = rng.randint(3, 12), rng.randint(4, 16)
            value = math.sqrt(a ** 2 + b ** 2)
            stem = (f"Two perpendicular forces of {a} N and {b} N act at a point. Find the magnitude of "
                    f"the resultant, to 2 decimal places.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b}, "expr": "sqrt(a**2+b**2)", "digits": 2}
            explain = f"For perpendicular forces the resultant is $\\sqrt{{{a}^2 + {b}^2}} = {fmt(value)}$ N."
            latex = rf"R = \sqrt{{{a}^2 + {b}^2}} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (a + b, "Adds the magnitudes, which only holds if they act along the same line.", "wrong-operation"),
                (abs(a - b), "Subtracts the magnitudes.", "wrong-operation"),
                (a ** 2 + b ** 2, "Omits the square root.", "missing-step"),
                (math.sqrt(a * b), "Takes the root of the product.", "wrong-operation")])
        elif depth == 2:
            a, b = rng.randint(3, 12), rng.randint(3, 12)
            value = math.degrees(math.atan(b / a))
            stem = (f"A vector has components {a} along $x$ and {b} along $y$. Find the angle it makes "
                    f"with the $x$-axis, in degrees to 2 decimal places.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b}, "expr": "degrees(atan(b/a))", "digits": 2}
            explain = f"$\\tan\\theta = {b}/{a}$, so $\\theta = \\tan^{{-1}}({fmt(b / a, 4)}) = {fmt(value)}^\\circ$."
            latex = rf"\theta = \tan^{{-1}}\left(\frac{{{b}}}{{{a}}}\right) = {fmt(value)}"
            correct, wrong = build(value, "°", [
                (math.degrees(math.atan(a / b)), "Inverts the ratio, giving the angle to the $y$-axis.", "inverted-ratio"),
                (math.atan(b / a), "Leaves the answer in radians.", "unit-error"),
                (math.degrees(math.asin(b / math.sqrt(a ** 2 + b ** 2))) + 5, "Misapplies the sine ratio.", "wrong-ratio"),
                (b / a, "Reports the ratio, not the angle.", "partial-answer")])
        else:
            a, b, angle = rng.randint(5, 14), rng.randint(5, 14), rng.choice([35, 50, 65, 110])
            value = math.sqrt(a ** 2 + b ** 2 + 2 * a * b * math.cos(math.radians(angle)))
            stem = (f"Two forces of {a} N and {b} N act at {angle}° to each other. Find the magnitude of "
                    f"the resultant, to 2 decimal places.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "t": angle},
                    "expr": "sqrt(a**2+b**2+2*a*b*cos(radians(t)))", "digits": 2}
            explain = (f"$R = \\sqrt{{{a}^2 + {b}^2 + 2({a})({b})\\cos {angle}^\\circ}} = {fmt(value)}$ N.")
            latex = rf"R = \sqrt{{{a}^2 + {b}^2 + 2 \times {a} \times {b} \cos {angle}^\circ}} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (math.sqrt(abs(a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(angle)))), "Subtracts the cosine term, which applies to the difference.", "sign-error"),
                (a + b, "Adds the magnitudes, ignoring the angle.", "missing-step"),
                (math.sqrt(a ** 2 + b ** 2), "Treats the forces as perpendicular.", "missing-step"),
                (math.sqrt(abs(a ** 2 + b ** 2 + 2 * a * b * math.cos(angle))), "Uses the angle in radians.", "unit-error")])

    elif domain == "limits":
        if depth == 0:
            a, b, c = rng.randint(2, 5), rng.randint(1, 6), rng.randint(1, 9)
            x0 = rng.randint(1, 4)
            value = a * x0 ** 2 + b * x0 + c
            stem = (f"Evaluate $\\lim_{{x \\to {x0}}} ({a}x^2 + {b}x + {c})$.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c, "x": x0},
                    "expr": "a*x**2+b*x+c", "digits": 2}
            explain = (f"The expression is a polynomial, which is continuous everywhere, so the "
                       f"limit is just its value there: ${a}({x0})^2 + {b}({x0}) + {c} = "
                       f"{fmt(value)}$.")
            latex = rf"\lim_{{x \to {x0}}} = {a}({x0})^2 + {b}({x0}) + {c} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (a * x0 + b * x0 + c, "Forgets to square the first term.", "missing-step"),
                (a * x0 ** 2 + b * x0, "Drops the constant.", "missing-step"),
                (c, "Substitutes zero instead of the stated value.", "wrong-rule")])
        elif depth == 1:
            a = rng.choice([2, 3, 4, 5, 6])
            value = 2 * a
            stem = (f"Evaluate $\\lim_{{x \\to {a}}} \\dfrac{{x^2 - {a * a}}}{{x - {a}}}$.")
            spec = {"kind": "compute", "vars": {"a": a}, "expr": "2*a", "digits": 2}
            explain = (f"Substituting gives $0/0$, so factor first: $x^2 - {a * a} = "
                       f"(x - {a})(x + {a})$, and the $(x - {a})$ cancels. What is left is "
                       f"$x + {a}$, which at $x = {a}$ is {fmt(value)}.")
            latex = rf"\lim_{{x \to {a}}} \frac{{(x-{a})(x+{a})}}{{x-{a}}} = {a}+{a} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (0, "Reads 0/0 as zero rather than as undetermined.", "wrong-rule"),
                (a, "Cancels to x rather than to x plus a.", "missing-step"),
                (a * a, "Stops at the numerator's constant.", "partial-answer")])
        elif depth == 2:
            k, m = rng.choice([2, 3, 5, 7]), rng.choice([2, 3, 4, 6])
            value = k / m
            stem = f"Evaluate $\\lim_{{x \\to 0}} \\dfrac{{\\sin {k}x}}{{{m}x}}$."
            spec = {"kind": "compute", "vars": {"k": k, "m": m}, "expr": "k/m", "digits": 4}
            explain = (f"As $x \\to 0$, $\\sin {k}x$ behaves like ${k}x$, so the ratio tends to "
                       f"${k}/{m} = {fmt(value, 4)}$. The standard result is "
                       f"$\\lim_{{u \\to 0}} \\frac{{\\sin u}}{{u}} = 1$, applied with $u = {k}x$.")
            latex = rf"\lim_{{x \to 0}} \frac{{\sin {k}x}}{{{m}x}} = \frac{{{k}}}{{{m}}} = {fmt(value, 4)}"
            correct, wrong = build(value, "", [
                (m / k, "Inverts the ratio.", "inverted-operation"),
                (1, "Applies the standard result without the two coefficients.", "missing-step"),
                (k * m, "Multiplies the coefficients.", "wrong-operation")], digits=4)
        else:
            # Chosen so that neither difference can be zero, rather than drawn
            # and retried: a loop that only redrew one of them spun forever
            # whenever the other pair collided.
            d = rng.choice([1, 2])
            b = rng.choice([1, 2])
            a = rng.choice([x for x in (2, 3, 4, 5) if x != b])
            c = rng.choice([x for x in (3, 4, 5, 6) if x != d])
            value = (a - b) / (c - d)
            stem = (f"Evaluate $\\lim_{{x \\to 0}} \\dfrac{{\\tan {a}x - {b}x}}{{{c}x - "
                    f"\\sin {d}x}}$.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c, "d": d},
                    "expr": "(a-b)/(c-d)", "digits": 4}
            explain = (f"Near zero $\\tan {a}x$ behaves like ${a}x$ and $\\sin {d}x$ like ${d}x$, "
                       f"so the top is $({a} - {b})x$ and the bottom $({c} - {d})x$. The $x$ "
                       f"cancels, leaving $\\frac{{{a - b}}}{{{c - d}}} = {fmt(value, 4)}$.")
            latex = rf"\frac{{{a}-{b}}}{{{c}-{d}}} = {fmt(value, 4)}"
            correct, wrong = build(value, "", [
                ((c - d) / (a - b), "Inverts the ratio.", "inverted-operation"),
                (a / c, "Uses only the leading coefficients and drops the other terms.", "missing-step"),
                (0, "Reads 0/0 as zero.", "wrong-rule")], digits=4)

    elif domain == "quadratic":
        if depth == 0:
            r1, r2 = rng.choice([1, 2, 3, 4]), rng.choice([5, 6, 7, 8])
            b, c = -(r1 + r2), r1 * r2
            value = r2
            stem = (f"Solve $x^2 {'+' if b >= 0 else '-'} {abs(b)}x + {c} = 0$ and give the "
                    f"larger root.")
            spec = {"kind": "compute", "vars": {"b": b, "c": c},
                    "expr": "(-b+sqrt(b**2-4*c))/2", "digits": 2}
            explain = (f"The formula gives $x = \\frac{{{-b} \\pm \\sqrt{{{b * b} - {4 * c}}}}}{{2}}$, "
                       f"so the roots are {r1} and {r2}. The larger is {r2}. Checking by factors: "
                       f"$(x - {r1})(x - {r2})$ expands to the original.")
            latex = rf"x = \frac{{-b \pm \sqrt{{b^2-4ac}}}}{{2a}} \Rightarrow {r1},\, {r2}"
            correct, wrong = build(value, "", [
                (r1, "Gives the smaller root.", "partial-answer"),
                (r1 + r2, "Reports the sum of the roots.", "wrong-rule"),
                (-r2, "Reverses the sign.", "sign-error")])
        elif depth == 1:
            a, b, c = rng.choice([1, 2]), rng.choice([4, 6, 8, 10]), rng.choice([1, 2, 3, 5])
            value = b * b - 4 * a * c
            stem = (f"What is the discriminant of ${a}x^2 + {b}x + {c} = 0$?")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c},
                    "expr": "b**2-4*a*c", "digits": 2}
            explain = (f"The discriminant is $b^2 - 4ac = {b}^2 - 4({a})({c}) = {fmt(value)}$. "
                       f"It is {'positive, so there are two distinct real roots' if value > 0 else 'not positive, so the roots are not two distinct real numbers'}.")
            latex = rf"b^2-4ac = {b}^2 - 4({a})({c}) = {fmt(value)}"
            correct, wrong = build(value, "", [
                (b * b + 4 * a * c, "Adds instead of subtracting.", "sign-error"),
                (b * b - 4 * c, "Leaves the leading coefficient out.", "missing-step"),
                (b * b - a * c, "Omits the factor of four.", "missing-step")])
        elif depth == 2:
            v0 = rng.choice([49, 98, 147])
            t1 = rng.choice([2, 3, 5])
            height = v0 * t1 - 4.9 * t1 ** 2
            value = t1
            stem = (f"A rocket is launched vertically with an initial velocity of {v0} m/s, so its "
                    f"height is $h(t) = {v0}t - 4.9t^2$ metres. At which earlier time is it "
                    f"{fmt(height)} m above the ground, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"v": v0, "h": height},
                    "expr": "(v-sqrt(v**2-4*4.9*h))/(2*4.9)", "digits": 2}
            explain = (f"Set $h(t) = {fmt(height)}$, which gives $4.9t^2 - {v0}t + {fmt(height)} = "
                       f"0$. The formula gives two times, one on the way up and one on the way "
                       f"down; the earlier is {fmt(value)} s.")
            latex = rf"t = \frac{{{v0} - \sqrt{{{v0}^2 - 4(4.9)({fmt(height)})}}}}{{2(4.9)}} = {fmt(value)}"
            later = (v0 + math.sqrt(v0 ** 2 - 4 * 4.9 * height)) / 9.8
            correct, wrong = build(value, " s", [
                (later, "Gives the later time, on the way down.", "partial-answer"),
                (height / v0, "Divides the height by the launch speed.", "wrong-rule"),
                (v0 / 9.8, "Gives the time to the top instead.", "wrong-rule")])
        else:
            h0, u = rng.choice([1.5, 3.0, 5.0]), rng.choice([0.6, 1.2, 2.0])
            g = 4.905
            value = (u + math.sqrt(u ** 2 + 4 * g * h0)) / (2 * g)
            stem = (f"A diver leaves a board {h0:g} m above the water moving upwards at {u:g} m/s, "
                    f"so their height is $h(t) = -{g}t^2 + {u:g}t + {h0:g}$ metres. How long "
                    f"until they reach the water, to 3 decimal places?")
            spec = {"kind": "compute", "vars": {"u": u, "h": h0, "g": g},
                    "expr": "(u+sqrt(u**2+4*g*h))/(2*g)", "digits": 3}
            explain = (f"The water is $h = 0$, so $-{g}t^2 + {u:g}t + {h0:g} = 0$. The formula "
                       f"gives one positive and one negative time; only the positive one happens, "
                       f"and it is {fmt(value, 3)} s.")
            latex = rf"t = \frac{{{u:g} + \sqrt{{{u:g}^2 + 4({g})({h0:g})}}}}{{2({g})}} = {fmt(value, 3)}"
            correct, wrong = build(value, " s", [
                ((u - math.sqrt(u ** 2 + 4 * g * h0)) / (2 * g), "Takes the negative root, which is before the jump.", "sign-error"),
                (math.sqrt(2 * h0 / 9.81), "Ignores the upward push and treats it as a free drop.", "missing-step"),
                (h0 / u, "Divides the height by the launch speed.", "wrong-rule")], digits=3)

    elif domain == "matrices":
        if depth == 0:
            # A singular matrix gives a determinant of zero, and every
            # distractor built by scaling it collapses onto zero too.
            for _ in range(40):
                a, b, c, d = (rng.randint(2, 9), rng.randint(1, 8),
                              rng.randint(1, 7), rng.randint(2, 9))
                if a * d != b * c:
                    break
            value = a * d - b * c
            stem = (f"Find the determinant of $\\begin{{vmatrix}} {a} & {b} \\\\ {c} & {d} "
                    f"\\end{{vmatrix}}$.")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c, "d": d},
                    "expr": "a*d-b*c", "digits": 2}
            explain = (f"For a two-by-two it is the leading diagonal less the other: "
                       f"${a}({d}) - {b}({c}) = {fmt(value)}$.")
            latex = rf"ad - bc = {a}({d}) - {b}({c}) = {fmt(value)}"
            correct, wrong = build(value, "", [
                (a * d + b * c, "Adds the two products.", "sign-error"),
                (b * c - a * d, "Takes the diagonals the wrong way round.", "sign-error"),
                (a * b - c * d, "Multiplies along the rows instead of the diagonals.", "wrong-rule")])
        elif depth == 1:
            for _ in range(40):
                m = [[rng.randint(-5, 5) for _ in range(3)] for _ in range(3)]
                m[0][0] = m[0][0] or 2
                value = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                         - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                         + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
                if value:
                    break
            rows = " \\\\ ".join(" & ".join(str(x) for x in r) for r in m)
            stem = f"Find the determinant of $\\begin{{vmatrix}} {rows} \\end{{vmatrix}}$."
            spec = {"kind": "compute",
                    "vars": {f"m{i}{j}": m[i][j] for i in range(3) for j in range(3)},
                    "expr": ("m00*(m11*m22-m12*m21)-m01*(m10*m22-m12*m20)"
                             "+m02*(m10*m21-m11*m20)"), "digits": 2}
            explain = (f"Expanding along the top row, with the signs $+\\,-\\,+$: "
                       f"${m[0][0]}({m[1][1]}\\cdot{m[2][2]} - {m[1][2]}\\cdot{m[2][1]}) "
                       f"- {m[0][1]}({m[1][0]}\\cdot{m[2][2]} - {m[1][2]}\\cdot{m[2][0]}) "
                       f"+ {m[0][2]}({m[1][0]}\\cdot{m[2][1]} - {m[1][1]}\\cdot{m[2][0]}) = "
                       f"{fmt(value)}$. The middle sign is the one most often dropped.")
            latex = rf"\det = {fmt(value)}"
            correct, wrong = build(value, "", [
                (value + 2 * m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]),
                 "Adds the middle term instead of subtracting it.", "sign-error"),
                (-value, "Reverses every sign.", "sign-error"),
                (m[0][0] * m[1][1] * m[2][2], "Multiplies the leading diagonal only.", "wrong-rule")])
        elif depth == 2:
            x = rng.choice([2, 3, 4, 5])
            value = 1 / (2 * x)
            stem = (f"For $A = \\begin{{pmatrix}} {2 * x} & 0 \\\\ {x} & {x} \\end{{pmatrix}}$, "
                    f"what is the top-left entry of $A^{{-1}}$, to 4 decimal places?")
            spec = {"kind": "compute", "vars": {"x": x}, "expr": "1/(2*x)", "digits": 4}
            explain = (f"The determinant is ${2 * x}({x}) - 0({x}) = {2 * x * x}$, and the inverse "
                       f"of $\\begin{{pmatrix}} a & b \\\\ c & d \\end{{pmatrix}}$ is "
                       f"$\\frac{{1}}{{ad-bc}}\\begin{{pmatrix}} d & -b \\\\ -c & a "
                       f"\\end{{pmatrix}}$. The top-left entry becomes $d/\\det = {x}/{2 * x * x} = "
                       f"{fmt(value, 4)}$.")
            latex = rf"\frac{{d}}{{\det}} = \frac{{{x}}}{{{2 * x * x}}} = {fmt(value, 4)}"
            correct, wrong = build(value, "", [
                (2 * x, "Reports the original entry rather than the inverse's.", "wrong-rule"),
                (1 / (2 * x * x), "Divides one by the determinant and stops.", "missing-step"),
                (x, "Takes d without dividing by the determinant.", "missing-step")], digits=4)
        else:
            r, c = rng.choice([2, 3, 4]), rng.choice([5, 6, 7])
            value = r
            stem = (f"$A$ is a ${r} \\times {c}$ matrix and $B$ is such that both $A^TB$ and "
                    f"$BA^T$ are defined. How many rows does $B$ have?")
            spec = {"kind": "compute", "vars": {"r": r}, "expr": "r", "digits": 0}
            explain = (f"$A^T$ is ${c} \\times {r}$. For $A^TB$ to be defined, $B$ must have as "
                       f"many rows as $A^T$ has columns, which is {r}. For $BA^T$ to be defined "
                       f"too, $B$ must have {c} columns, so $B$ is the same shape as $A$: "
                       f"${r} \\times {c}$.")
            latex = rf"A^T \text{{ is }} {c} \times {r} \Rightarrow B \text{{ is }} {r} \times {c}"
            correct, wrong = build(value, "", [
                (c, "Gives the number of columns instead.", "wrong-term"),
                (r * c, "Multiplies the two dimensions.", "wrong-operation"),
                (c - r, "Subtracts the dimensions.", "wrong-operation")], digits=0)

    elif domain == "dotcross":
        # Redrawn until both products this sub-topic asks about are non-zero,
        # for the same reason as the determinants above.
        for _ in range(60):
            p = [rng.randint(-4, 5) for _ in range(3)]
            q = [rng.randint(-4, 5) for _ in range(3)]
            if sum(a * b for a, b in zip(p, q)) and (p[2] * q[0] - p[0] * q[2]):
                break
        if depth == 0:
            value = sum(a * b for a, b in zip(p, q))
            stem = (f"Find the scalar product $\\mathbf{{p}} \\cdot \\mathbf{{q}}$ when "
                    f"$\\mathbf{{p}} = {vec(p)}$ and $\\mathbf{{q}} = {vec(q)}$.")
            spec = {"kind": "compute",
                    "vars": {"p0": p[0], "p1": p[1], "p2": p[2],
                             "q0": q[0], "q1": q[1], "q2": q[2]},
                    "expr": "p0*q0+p1*q1+p2*q2", "digits": 2}
            explain = (f"Multiply matching components and add: "
                       f"$({p[0]})({q[0]}) + ({p[1]})({q[1]}) + ({p[2]})({q[2]}) = {fmt(value)}$. "
                       f"The result is a number, not a vector.")
            latex = rf"\mathbf{{p}} \cdot \mathbf{{q}} = {fmt(value)}"
            correct, wrong = build(value, "", [
                (p[0] * q[0] + p[1] * q[1], "Leaves the k components out.", "missing-step"),
                (sum(p) + sum(q), "Adds the components instead of multiplying them.", "wrong-operation"),
                (p[0] * q[0] - p[1] * q[1] + p[2] * q[2], "Alternates the signs, as a determinant would.", "wrong-rule")])
        elif depth == 1:
            cross = [p[1] * q[2] - p[2] * q[1],
                     p[2] * q[0] - p[0] * q[2],
                     p[0] * q[1] - p[1] * q[0]]
            # Asked for the j component rather than the whole vector. The paper
            # offers four vectors and asks which one it is, but a vector cannot
            # be handed to a validator that recomputes a number -- and the j
            # component is the one worth asking for, because its sign is the
            # trap in the expansion.
            value = cross[1]
            stem = (f"Given $\\mathbf{{p}} = {vec(p)}$ and $\\mathbf{{q}} = {vec(q)}$, what is "
                    f"the $\\mathbf{{j}}$ component of $\\mathbf{{p}} \\times \\mathbf{{q}}$?")
            spec = {"kind": "compute",
                    "vars": {"p0": p[0], "p2": p[2], "q0": q[0], "q2": q[2]},
                    "expr": "p2*q0-p0*q2", "digits": 2}
            explain = (f"Expanding along the top row, the $\\mathbf{{j}}$ term carries a minus "
                       f"sign: $-({p[0]}\\cdot{q[2]} - {p[2]}\\cdot{q[0]}) = {fmt(value)}$. "
                       f"The whole product is ${vec(cross)}$.")
            latex = rf"\mathbf{{p}} \times \mathbf{{q}} = {vec(cross)}"
            correct, wrong = build(value, "", [
                (-value, "Keeps the middle term positive, which is the usual slip.", "sign-error"),
                (cross[0], "Gives the i component instead.", "wrong-term"),
                (cross[2], "Gives the k component instead.", "wrong-term"),
                (p[1] * q[1], "Multiplies the matching components, which is neither product.", "wrong-rule")])
        elif depth == 2:
            # Built from a chosen angle, so the answer is a round number of
            # degrees rather than whatever two random vectors happen to give.
            deg = rng.choice([30, 45, 60, 120, 135])
            m1, m2 = rng.choice([3, 4, 5, 6]), rng.choice([2, 5, 8, 10])
            dot = m1 * m2 * math.cos(math.radians(deg))
            value = deg
            stem = (f"Two vectors have magnitudes {m1} and {m2}, and their scalar product is "
                    f"{fmt(dot)}. What is the angle between them, in degrees?")
            spec = {"kind": "compute", "vars": {"d": dot, "a": m1, "b": m2},
                    "expr": "degrees(acos(d/(a*b)))", "digits": 2}
            explain = (f"From $\\mathbf{{a}} \\cdot \\mathbf{{b}} = |a||b|\\cos\\theta$, "
                       f"$\\cos\\theta = \\frac{{{fmt(dot)}}}{{{m1} \\times {m2}}} = "
                       f"{fmt(dot / (m1 * m2), 4)}$, so $\\theta = {fmt(value)}°$. A negative "
                       f"scalar product means an obtuse angle.")
            latex = rf"\theta = \cos^{{-1}}\frac{{{fmt(dot)}}}{{{m1}\times{m2}}} = {fmt(value)}°"
            correct, wrong = build(value, "°", [
                (180 - deg, "Takes the supplement.", "wrong-rule"),
                (90, "Assumes perpendicular, which only holds when the product is zero.", "wrong-rule"),
                (math.degrees(math.asin(min(1, abs(dot / (m1 * m2))))), "Uses the sine instead of the cosine.", "wrong-rule")])
        else:
            deg = rng.choice([60, 90, 120])
            m1, m2 = rng.choice([3, 4, 5]), rng.choice([5, 6, 7])
            third = math.sqrt(m1 ** 2 + m2 ** 2 + 2 * m1 * m2 * math.cos(math.radians(deg)))
            value = deg
            stem = (f"Three vectors satisfy $\\alpha + \\beta + \\gamma = \\mathbf{{0}}$, with "
                    f"$|\\alpha| = {m1}$, $|\\beta| = {m2}$ and $|\\gamma| = {fmt(third)}$. What "
                    f"is the angle between $\\alpha$ and $\\beta$, in degrees?")
            spec = {"kind": "compute", "vars": {"a": m1, "b": m2, "c": third},
                    "expr": "degrees(acos((c**2-a**2-b**2)/(2*a*b)))", "digits": 2}
            explain = (f"Since $\\gamma = -(\\alpha + \\beta)$, squaring gives "
                       f"$|\\gamma|^2 = |\\alpha|^2 + |\\beta|^2 + 2|\\alpha||\\beta|"
                       f"\\cos\\theta$. So $\\cos\\theta = "
                       f"\\frac{{{fmt(third * third)} - {m1 * m1} - {m2 * m2}}}{{2({m1})({m2})}}$, "
                       f"giving $\\theta = {fmt(value)}°$.")
            latex = rf"\cos\theta = \frac{{|\gamma|^2-|\alpha|^2-|\beta|^2}}{{2|\alpha||\beta|}} \Rightarrow {fmt(value)}°"
            correct, wrong = build(value, "°", [
                (180 - deg, "Takes the supplement, as though the sum were a difference.", "sign-error"),
                (90, "Assumes the triangle is right-angled.", "wrong-rule"),
                (math.degrees(math.acos(max(-1, min(1, (m1 ** 2 + m2 ** 2 - third ** 2) / (2 * m1 * m2))))),
                 "Uses the cosine rule for a closing side rather than for a sum.", "sign-error")])

    else:
        # Every sub-topic in the catalogue needs a branch here, or the seeder
        # would fail on an unbound name rather than saying what is missing.
        raise ValueError(f"no Mathematics template for {domain!r}")

    return stem, correct, explain, wrong, spec, latex
