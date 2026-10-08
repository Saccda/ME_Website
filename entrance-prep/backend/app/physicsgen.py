"""Physics templates, one family per domain and difficulty.

The Physics section of the entrance examination is electrical: Ohm's law,
charge and current, resistor networks, power and energy, work and potential,
capacitance, and the units and instruments that go with them. These templates
follow that scope.

Almost every answer is computable, so each template declares the computation it
is built from and `validate` recomputes it rather than trusting the key. The
conceptual questions -- which unit, which instrument -- declare a key into a
reviewed table instead, which is checkable in the same way.

Numbers, wording and distractors are generated here. No question is copied from
any paper or book, and figures are never referenced, because a generated
question cannot ship a circuit diagram.

Values are computed in the unit they are displayed in, so a question about
microfarads computes in microfarads. The validator compares the number it
recomputes against the number in the keyed option, so the two must agree.
"""
import math

from .mathgen import build, fmt


def _a(n):
    """"a" or "an" before a number, chosen by how the number is spoken.

    Eight, eleven and eighteen begin with a vowel sound, as do the eighties.
    Everything else these templates draw takes "a". Without this they produced
    "An 12 Ω" and "a 8 Ω resistor".
    """
    whole = abs(int(n))
    return "an" if whole in (8, 11, 18) or 80 <= whole <= 89 else "a"


def template(domain, depth, rng):
    """Return stem, answer, explanation, distractors, validator spec and LaTeX."""
    if domain == "current":
        if depth == 0:
            i, t = rng.choice([1.5, 2.3, 3.0, 4.5]), rng.choice([10, 20, 30, 60])
            value = i * t
            stem = (f"A steady current of {fmt(i)} A flows through a conductor for {t} s. "
                    f"How much charge passes a given cross-section?")
            spec = {"kind": "compute", "vars": {"i": i, "t": t}, "expr": "i*t", "digits": 2}
            explain = f"Charge is current times time: $Q = It = {fmt(i)} \\times {t} = {fmt(value)}$ C."
            latex = rf"Q = It = {fmt(i)} \times {t} = {fmt(value)}"
            correct, wrong = build(value, " C", [
                (i / t, "Divides current by time instead of multiplying.", "inverted-operation"),
                (t / i, "Divides time by current.", "inverted-operation"),
                (i + t, "Adds the two quantities.", "wrong-operation"),
                (i * t / 60, "Treats the time as minutes.", "unit-error")])
        elif depth == 1:
            q, t = rng.choice([24, 36, 50, 72]), rng.choice([4, 6, 8, 12])
            value = q / t
            stem = (f"A charge of {q} C passes a point in {t} s. What is the current?")
            spec = {"kind": "compute", "vars": {"q": q, "t": t}, "expr": "q/t", "digits": 2}
            explain = f"Current is charge per second: $I = Q/t = {q} \\div {t} = {fmt(value)}$ A."
            latex = rf"I = \frac{{Q}}{{t}} = \frac{{{q}}}{{{t}}} = {fmt(value)}"
            correct, wrong = build(value, " A", [
                (q * t, "Multiplies instead of dividing.", "inverted-operation"),
                (t / q, "Divides time by charge.", "inverted-operation"),
                (q - t, "Subtracts the time from the charge.", "wrong-operation"),
                (q / t / 60, "Converts to minutes, which the question does not ask for.", "unit-error")])
        elif depth == 2:
            a, b = rng.randint(2, 9), rng.randint(3, 12)
            value = a
            stem = (f"The charge through a circuit element is $q(t) = ({a}t + {b})$ mC, with $t$ in "
                    f"seconds. What is the current through the element?")
            spec = {"kind": "compute", "vars": {"a": a}, "expr": "a", "digits": 2}
            explain = (f"Current is the rate of change of charge. The charge rises by {a} mC every "
                       f"second, so the current is a steady {a} mA. The constant {b} mC is the charge "
                       f"already present at $t = 0$ and does not add to the rate.")
            latex = rf"i = \frac{{dq}}{{dt}} = \frac{{d}}{{dt}}({a}t + {b}) = {a}"
            correct, wrong = build(value, " mA", [
                (a + b, "Adds the constant term to the rate.", "extra-term"),
                (b, "Reports the constant term instead of the rate.", "wrong-term"),
                (a * b, "Multiplies the two coefficients.", "wrong-operation"),
                (a / 2, "Halves the rate.", "arithmetic-slip")])
        else:
            i, minutes = rng.choice([0.25, 0.4, 0.75, 1.2]), rng.choice([3, 5, 10, 15])
            value = i * minutes * 60
            stem = (f"A device draws {fmt(i)} A for {minutes} minutes. What total charge has passed "
                    f"through it?")
            spec = {"kind": "compute", "vars": {"i": i, "m": minutes}, "expr": "i*m*60", "digits": 2}
            explain = (f"Convert the time to seconds first: {minutes} min $= {minutes * 60}$ s. "
                       f"Then $Q = It = {fmt(i)} \\times {minutes * 60} = {fmt(value)}$ C.")
            latex = rf"Q = It = {fmt(i)} \times ({minutes} \times 60) = {fmt(value)}"
            correct, wrong = build(value, " C", [
                (i * minutes, "Leaves the time in minutes.", "unit-error"),
                (i * minutes * 3600, "Converts minutes to seconds twice.", "unit-error"),
                (minutes * 60 / i, "Divides the time by the current.", "inverted-operation"),
                (i + minutes * 60, "Adds the time to the current.", "wrong-operation")])

    elif domain == "ohm":
        if depth == 0:
            r, v = rng.choice([11, 22, 44, 55]), rng.choice([110, 220, 240])
            value = v / r
            stem = (f"{_a(r).capitalize()} {r} Ω resistive heater is connected across "
                    f"{_a(v)} {v} V supply. What current flows through the heater?")
            spec = {"kind": "compute", "vars": {"v": v, "r": r}, "expr": "v/r", "digits": 2}
            explain = f"Ohm's law rearranged for current: $I = V/R = {v} \\div {r} = {fmt(value)}$ A."
            latex = rf"I = \frac{{V}}{{R}} = \frac{{{v}}}{{{r}}} = {fmt(value)}"
            correct, wrong = build(value, " A", [
                (v * r, "Multiplies voltage by resistance.", "inverted-operation"),
                (r / v, "Divides resistance by voltage.", "inverted-operation"),
                (v - r, "Subtracts resistance from voltage.", "wrong-operation"),
                (v / r / 10, "A slip of one power of ten.", "scale-error")])
        elif depth == 1:
            r, i = rng.choice([8, 12, 15, 18]), rng.choice([3, 5, 7, 11])
            value = i * r
            stem = (f"A resistor of {r} Ω carries a current of {i} A. "
                    f"What is the voltage across the resistor?")
            spec = {"kind": "compute", "vars": {"i": i, "r": r}, "expr": "i*r", "digits": 2}
            explain = f"Ohm's law: $V = IR = {i} \\times {r} = {fmt(value)}$ V."
            latex = rf"V = IR = {i} \times {r} = {fmt(value)}"
            correct, wrong = build(value, " V", [
                (i / r, "Divides current by resistance.", "inverted-operation"),
                (r / i, "Divides resistance by current.", "inverted-operation"),
                (i + r, "Adds the two quantities.", "wrong-operation"),
                (i * r / 2, "Halves the result.", "arithmetic-slip")])
        elif depth == 2:
            v, i = rng.choice([12, 24, 48, 60]), rng.choice([0.5, 1.5, 2.5, 4.0])
            value = v / i
            stem = (f"A component draws {fmt(i)} A when {v} V is applied across it. "
                    f"What is its resistance?")
            spec = {"kind": "compute", "vars": {"v": v, "i": i}, "expr": "v/i", "digits": 2}
            explain = f"Ohm's law rearranged for resistance: $R = V/I = {v} \\div {fmt(i)} = {fmt(value)}$ Ω."
            latex = rf"R = \frac{{V}}{{I}} = \frac{{{v}}}{{{fmt(i)}}} = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (v * i, "Multiplies instead of dividing.", "inverted-operation"),
                (i / v, "Divides current by voltage, which gives conductance.", "inverted-operation"),
                (v - i, "Subtracts the current from the voltage.", "wrong-operation"),
                (v / i / 2, "Halves the result.", "arithmetic-slip")])
        else:
            v, p = rng.choice([110, 230, 240]), rng.choice([40, 60, 100, 200])
            value = v ** 2 / p
            stem = (f"A lamp rated {p} W operates from a {v} V supply. "
                    f"What is the resistance of its filament, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"v": v, "p": p}, "expr": "v**2/p", "digits": 2}
            explain = (f"Power and resistance are linked by $P = V^2/R$, so $R = V^2/P = "
                       f"{v}^2 \\div {p} = {fmt(value)}$ Ω.")
            latex = rf"R = \frac{{V^2}}{{P}} = \frac{{{v}^2}}{{{p}}} = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (v / p, "Omits the square on the voltage.", "missing-step"),
                (p / v, "Inverts the relationship.", "inverted-operation"),
                (p / v ** 2, "Inverts the whole expression.", "inverted-operation"),
                (v ** 2 * p, "Multiplies by the power instead of dividing.", "inverted-operation")])

    elif domain == "networks":
        if depth == 0:
            a, b = rng.choice([4, 8, 12, 15]), rng.choice([3, 6, 9, 20])
            value = a + b
            stem = (f"{_a(a).capitalize()} {a} Ω and {_a(b)} {b} Ω resistor are connected in "
                    f"series. What is the total resistance of the circuit?")
            spec = {"kind": "compute", "vars": {"a": a, "b": b}, "expr": "a+b", "digits": 2}
            explain = f"Resistances in series add: ${a} + {b} = {fmt(value)}$ Ω."
            latex = rf"R_T = R_1 + R_2 = {a} + {b} = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (a * b / (a + b), "Uses the parallel formula instead.", "wrong-rule"),
                (abs(a - b), "Subtracts the resistances.", "wrong-operation"),
                (a * b, "Multiplies the resistances.", "wrong-operation"),
                ((a + b) / 2, "Averages the resistances.", "wrong-operation")])
        elif depth == 1:
            a, b = rng.choice([4, 6, 10, 12]), rng.choice([3, 8, 15, 24])
            value = a * b / (a + b)
            stem = (f"{_a(a).capitalize()} {a} Ω and {_a(b)} {b} Ω resistor are connected in "
                    f"parallel. What is the equivalent resistance, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"a": a, "b": b}, "expr": "a*b/(a+b)", "digits": 2}
            explain = (f"For two resistors in parallel, $R = \\frac{{R_1 R_2}}{{R_1 + R_2}} = "
                       f"\\frac{{{a} \\times {b}}}{{{a} + {b}}} = {fmt(value)}$ Ω. It is always "
                       f"smaller than either resistor.")
            latex = rf"R = \frac{{{a} \times {b}}}{{{a} + {b}}} = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (a + b, "Adds them as though in series.", "wrong-rule"),
                (1 / a + 1 / b, "Stops at the sum of reciprocals without inverting.", "missing-step"),
                ((a + b) / (a * b), "Inverts the formula.", "inverted-operation"),
                ((a + b) / 2, "Averages the resistances.", "wrong-operation")])
        elif depth == 2:
            r1, r2, v = rng.choice([1, 2, 4]), rng.choice([3, 5, 8]), rng.choice([9, 12, 24])
            value = v * r2 / (r1 + r2)
            stem = (f"{_a(v).capitalize()} {v} V supply is connected across {_a(r1)} {r1} Ω and "
                    f"{_a(r2)} {r2} Ω resistor in series. What is the voltage across the {r2} Ω "
                    f"resistor, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"v": v, "a": r1, "b": r2},
                    "expr": "v*b/(a+b)", "digits": 2}
            explain = (f"The series current is $I = {v} \\div ({r1} + {r2})$. The voltage across "
                       f"{r2} Ω is that current times {r2} Ω, which is the divider rule "
                       f"$V \\times \\frac{{R_2}}{{R_1 + R_2}} = {fmt(value)}$ V.")
            latex = rf"V_2 = {v} \times \frac{{{r2}}}{{{r1} + {r2}}} = {fmt(value)}"
            correct, wrong = build(value, " V", [
                (v * r1 / (r1 + r2), "Uses the other resistor in the numerator.", "wrong-term"),
                (v / (r1 + r2), "Reports the current, not the voltage.", "partial-answer"),
                (v / r2, "Divides the supply by the resistance.", "wrong-rule"),
                (v / 2, "Splits the supply equally, which only holds for equal resistors.", "wrong-rule")])
        else:
            a, b, c = rng.choice([6, 10, 12]), rng.choice([3, 6, 12]), rng.choice([4, 8, 16])
            value = a * b / (a + b) + c
            stem = (f"{_a(a).capitalize()} {a} kΩ and {_a(b)} {b} kΩ resistor are connected in "
                    f"parallel, and that combination is in series with {_a(c)} {c} kΩ resistor. "
                    f"What is the total resistance, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "c": c},
                    "expr": "a*b/(a+b)+c", "digits": 2}
            explain = (f"Reduce the parallel pair first: $\\frac{{{a} \\times {b}}}{{{a} + {b}}} = "
                       f"{fmt(a * b / (a + b))}$ kΩ. That is in series with {c} kΩ, so the total is "
                       f"{fmt(value)} kΩ. Work from the innermost combination outwards.")
            latex = rf"R_T = \frac{{{a} \times {b}}}{{{a} + {b}}} + {c} = {fmt(value)}"
            correct, wrong = build(value, " kΩ", [
                (a + b + c, "Treats all three as being in series.", "wrong-rule"),
                (a * b / (a + b), "Stops at the parallel pair and omits the series resistor.", "missing-step"),
                (1 / (1 / a + 1 / b + 1 / c), "Treats all three as being in parallel.", "wrong-rule"),
                (a * b / (a + b) * c, "Multiplies by the series resistor instead of adding.", "wrong-operation")])

    elif domain == "power":
        if depth == 0:
            v, i = rng.choice([6, 12, 24, 230]), rng.choice([0.5, 2, 3, 5])
            value = v * i
            stem = (f"A {v} V supply delivers {fmt(i)} A to a load. What power does it supply?")
            spec = {"kind": "compute", "vars": {"v": v, "i": i}, "expr": "v*i", "digits": 2}
            explain = f"Power is voltage times current: $P = VI = {v} \\times {fmt(i)} = {fmt(value)}$ W."
            latex = rf"P = VI = {v} \times {fmt(i)} = {fmt(value)}"
            correct, wrong = build(value, " W", [
                (v / i, "Divides instead of multiplying.", "inverted-operation"),
                (i / v, "Divides current by voltage.", "inverted-operation"),
                (v + i, "Adds the two quantities.", "wrong-operation"),
                (v * i / 1000, "Reports kilowatts while the question asks for watts.", "unit-error")])
        elif depth == 1:
            i, r = rng.choice([0.5, 1.5, 2, 3]), rng.choice([3, 12, 25, 40])
            value = i ** 2 * r
            stem = (f"A current of {fmt(i)} A flows through {_a(r)} {r} Ω resistor. "
                    f"What power is dissipated in the resistor?")
            spec = {"kind": "compute", "vars": {"i": i, "r": r}, "expr": "i**2*r", "digits": 2}
            explain = (f"$P = I^2 R = {fmt(i)}^2 \\times {r} = {fmt(value)}$ W. The current is "
                       f"squared, so doubling it quadruples the heat.")
            latex = rf"P = I^2 R = {fmt(i)}^2 \times {r} = {fmt(value)}"
            correct, wrong = build(value, " W", [
                (i * r, "Omits the square on the current.", "missing-step"),
                (i * r ** 2, "Squares the resistance instead of the current.", "wrong-term"),
                (i ** 2 / r, "Divides by the resistance.", "inverted-operation"),
                (r / i ** 2, "Inverts the whole expression.", "inverted-operation")])
        elif depth == 2:
            w, hours = rng.choice([60, 100, 300, 500]), rng.choice([2, 4, 5, 8])
            value = w * hours / 1000
            stem = (f"A {w} W bulb burns for {hours} hours. "
                    f"What energy has it consumed, in kilowatt-hours?")
            spec = {"kind": "compute", "vars": {"w": w, "h": hours}, "expr": "w*h/1000", "digits": 3}
            explain = (f"Energy in kWh is power in kilowatts times time in hours: "
                       f"${w} \\div 1000 = {fmt(w / 1000, 3)}$ kW, and "
                       f"${fmt(w / 1000, 3)} \\times {hours} = {fmt(value, 3)}$ kWh.")
            latex = rf"E = \frac{{{w}}}{{1000}} \times {hours} = {fmt(value, 3)}"
            correct, wrong = build(value, " kWh", [
                (w * hours, "Leaves the power in watts.", "unit-error"),
                (w / hours / 1000, "Divides by the time instead of multiplying.", "inverted-operation"),
                (w * hours / 3600, "Converts using seconds in an hour.", "unit-error"),
                (w * hours / 100, "A slip of one power of ten in the conversion.", "scale-error")], digits=3)
        else:
            q, t, v = rng.choice([30, 50, 80, 120]), rng.choice([10, 20, 25, 40]), rng.choice([4, 6, 12, 24])
            value = q / t * v
            stem = (f"A charge of {q} C moves through a potential difference of {v} V in {t} s. "
                    f"What is the power?")
            spec = {"kind": "compute", "vars": {"q": q, "t": t, "v": v},
                    "expr": "q/t*v", "digits": 2}
            explain = (f"The current is $Q/t = {q} \\div {t} = {fmt(q / t)}$ A. Power is then "
                       f"$VI = {v} \\times {fmt(q / t)} = {fmt(value)}$ W. Equivalently, the work "
                       f"$QV$ divided by the time.")
            latex = rf"P = \frac{{Q}}{{t}} \times V = \frac{{{q}}}{{{t}}} \times {v} = {fmt(value)}"
            correct, wrong = build(value, " W", [
                (q * v, "Gives the total work in joules, not the power.", "partial-answer"),
                (q * v * t, "Multiplies by the time instead of dividing.", "inverted-operation"),
                (q / t, "Stops at the current.", "partial-answer"),
                (v / (q / t), "Divides voltage by current, giving resistance.", "wrong-rule")])

    elif domain == "work":
        if depth == 0:
            q, v = rng.choice([2, 4, 5, 8]), rng.choice([6, 12, 50, 200])
            value = q * v
            stem = (f"A charge of {q} C is moved through a potential difference of {v} V. "
                    f"How much work is done?")
            spec = {"kind": "compute", "vars": {"q": q, "v": v}, "expr": "q*v", "digits": 2}
            explain = f"Work is charge times potential difference: $W = QV = {q} \\times {v} = {fmt(value)}$ J."
            latex = rf"W = QV = {q} \times {v} = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (v / q, "Divides voltage by charge.", "inverted-operation"),
                (q / v, "Divides charge by voltage.", "inverted-operation"),
                (q + v, "Adds the two quantities.", "wrong-operation"),
                (q * v / 2, "Halves the result, as though storing energy in a capacitor.", "wrong-rule")])
        elif depth == 1:
            w, v = rng.choice([1, 2, 5, 10]), rng.choice([200, 250, 400, 500])
            value = w / v * 1000
            stem = (f"Moving an electric charge through a potential difference of {v} V does {w} J "
                    f"of work. What is the magnitude of the charge, in millicoulombs?")
            spec = {"kind": "compute", "vars": {"w": w, "v": v}, "expr": "w/v*1000", "digits": 2}
            explain = (f"Rearranging $W = QV$ gives $Q = W/V = {w} \\div {v} = "
                       f"{fmt(w / v, 5)}$ C, which is {fmt(value)} mC.")
            latex = rf"Q = \frac{{W}}{{V}} = \frac{{{w}}}{{{v}}} = {fmt(w / v, 5)}\,\text{{C}}"
            correct, wrong = build(value, " mC", [
                (w * v, "Multiplies instead of dividing.", "inverted-operation"),
                (v / w * 1000, "Divides voltage by work.", "inverted-operation"),
                (w / v, "Leaves the answer in coulombs.", "unit-error"),
                (w / v * 1e6, "Converts to microcoulombs instead.", "unit-error")])
        elif depth == 2:
            w, q = rng.choice([12, 24, 48, 60]), rng.choice([2, 3, 4, 6])
            value = w / q
            stem = (f"{w} J of work is done moving a charge of {q} C between two points. "
                    f"What is the potential difference between them?")
            spec = {"kind": "compute", "vars": {"w": w, "q": q}, "expr": "w/q", "digits": 2}
            explain = (f"Potential difference is work per unit charge: $V = W/Q = {w} \\div {q} = "
                       f"{fmt(value)}$ V.")
            latex = rf"V = \frac{{W}}{{Q}} = \frac{{{w}}}{{{q}}} = {fmt(value)}"
            correct, wrong = build(value, " V", [
                (w * q, "Multiplies instead of dividing.", "inverted-operation"),
                (q / w, "Divides charge by work.", "inverted-operation"),
                (w - q, "Subtracts the charge from the work.", "wrong-operation"),
                (w / q / 2, "Halves the result.", "arithmetic-slip")])
        else:
            v, i, minutes = rng.choice([12, 24, 230]), rng.choice([0.5, 2, 4]), rng.choice([5, 10, 30])
            value = v * i * minutes * 60
            stem = (f"A {v} V supply delivers {fmt(i)} A to a heater for {minutes} minutes. "
                    f"How much energy does the heater receive, in joules?")
            spec = {"kind": "compute", "vars": {"v": v, "i": i, "m": minutes},
                    "expr": "v*i*m*60", "digits": 2}
            explain = (f"Power is $VI = {v} \\times {fmt(i)} = {fmt(v * i)}$ W, and energy is power "
                       f"times time in seconds: $ {fmt(v * i)} \\times {minutes * 60} = {fmt(value)}$ J.")
            latex = rf"W = VIt = {v} \times {fmt(i)} \times ({minutes} \times 60) = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (v * i * minutes, "Leaves the time in minutes.", "unit-error"),
                (v * i, "Stops at the power.", "partial-answer"),
                (v * minutes * 60 / i, "Divides by the current.", "inverted-operation"),
                (v * i * minutes * 3600, "Converts minutes to seconds twice.", "unit-error")])

    elif domain == "capacitance":
        if depth == 0:
            q, v = rng.choice([20, 40, 60, 100]), rng.choice([5, 10, 20, 25])
            value = q / v
            stem = (f"A capacitor stores a charge of {q} μC when connected across a {v} V supply. "
                    f"What is its capacitance?")
            spec = {"kind": "compute", "vars": {"q": q, "v": v}, "expr": "q/v", "digits": 2}
            explain = (f"Capacitance is charge per volt: $C = Q/V = {q} \\div {v} = {fmt(value)}$ μF. "
                       f"Microcoulombs divided by volts gives microfarads directly.")
            latex = rf"C = \frac{{Q}}{{V}} = \frac{{{q}}}{{{v}}} = {fmt(value)}"
            correct, wrong = build(value, " μF", [
                (q * v, "Multiplies instead of dividing.", "inverted-operation"),
                (v / q, "Divides voltage by charge.", "inverted-operation"),
                (q - v, "Subtracts the voltage from the charge.", "wrong-operation"),
                (q / v / 2, "Halves the result.", "arithmetic-slip")])
        elif depth == 1:
            c, v = rng.choice([2, 4, 6, 10]), rng.choice([5, 9, 12, 20])
            value = c * v
            stem = (f"A {c} μF capacitor is connected across a {v} V supply. "
                    f"What charge does it store?")
            spec = {"kind": "compute", "vars": {"c": c, "v": v}, "expr": "c*v", "digits": 2}
            explain = f"Rearranging $C = Q/V$ gives $Q = CV = {c} \\times {v} = {fmt(value)}$ μC."
            latex = rf"Q = CV = {c} \times {v} = {fmt(value)}"
            correct, wrong = build(value, " μC", [
                (c / v, "Divides instead of multiplying.", "inverted-operation"),
                (v / c, "Divides voltage by capacitance.", "inverted-operation"),
                (c * v / 2, "Uses the energy formula's factor of a half.", "wrong-rule"),
                (c + v, "Adds the two quantities.", "wrong-operation")])
        elif depth == 2:
            c, v = rng.choice([2, 4, 6, 8]), rng.choice([3, 5, 10, 12])
            value = 0.5 * c * v ** 2
            stem = (f"A capacitor of {c} μF is charged to {v} V. "
                    f"What energy is stored in it?")
            spec = {"kind": "compute", "vars": {"c": c, "v": v}, "expr": "0.5*c*v**2", "digits": 2}
            explain = (f"$W = \\tfrac12 C V^2 = 0.5 \\times {c} \\times {v}^2 = {fmt(value)}$ μJ. "
                       f"The voltage is squared, so doubling it stores four times the energy.")
            latex = rf"W = \tfrac12 C V^2 = 0.5 \times {c} \times {v}^2 = {fmt(value)}"
            correct, wrong = build(value, " μJ", [
                (c * v ** 2, "Omits the factor of one half.", "missing-step"),
                (0.5 * c * v, "Omits the square on the voltage.", "missing-step"),
                (c * v, "Gives the stored charge instead of the energy.", "partial-answer"),
                (0.5 * c ** 2 * v, "Squares the capacitance instead of the voltage.", "wrong-term")])
        else:
            a, b, v = rng.choice([2, 4, 6]), rng.choice([3, 6, 12]), rng.choice([5, 10, 20])
            combined = a * b / (a + b)
            value = 0.5 * combined * v ** 2
            stem = (f"{_a(a).capitalize()} {a} μF and {_a(b)} {b} μF capacitor are connected in "
                    f"series across {_a(v)} {v} V supply. What total energy is stored, to 2 "
                    f"decimal places?")
            spec = {"kind": "compute", "vars": {"a": a, "b": b, "v": v},
                    "expr": "0.5*(a*b/(a+b))*v**2", "digits": 2}
            # The intermediate is shown to four places on purpose: rounded to
            # two it does not reproduce the final answer, and a student who
            # follows the explanation should arrive at the keyed value.
            explain = (f"Capacitors in series combine like resistors in parallel: "
                       f"$\\frac{{{a} \\times {b}}}{{{a} + {b}}} = {fmt(combined, 4)}$ μF. Then "
                       f"$W = \\tfrac12 C V^2 = 0.5 \\times {fmt(combined, 4)} \\times {v}^2 = "
                       f"{fmt(value)}$ μJ.")
            latex = rf"W = \tfrac12 \left(\frac{{{a} \times {b}}}{{{a} + {b}}}\right) {v}^2 = {fmt(value)}"
            correct, wrong = build(value, " μJ", [
                (0.5 * (a + b) * v ** 2, "Adds the capacitances, which is the parallel rule.", "wrong-rule"),
                (combined * v ** 2, "Omits the factor of one half.", "missing-step"),
                (0.5 * combined * v, "Omits the square on the voltage.", "missing-step"),
                (0.5 * a * v ** 2, "Uses only the first capacitor.", "missing-step")])

    elif domain == "quantities":
        if depth == 0:
            quantity = rng.choice(["electrical work", "electrical power", "conductance",
                                   "capacitance", "electric charge", "inductance"])
            stem = f"What is the SI unit of measurement for {quantity}?"
            spec = {"kind": "fact", "table": "si_units", "key": quantity}
            correct, wrong = _fact_options("si_units", quantity, rng)
            explain = (f"The SI unit of {quantity} is the {correct}. Learning each quantity with "
                       f"its unit makes a wrong unit in an answer easy to spot.")
            latex = None
        elif depth == 1:
            instrument = rng.choice(["An ammeter", "A voltmeter", "An ohmmeter", "A wattmeter"])
            stem = f"{instrument} is used to measure which quantity?"
            spec = {"kind": "fact", "table": "measured_by", "key": instrument}
            correct, wrong = _fact_options("measured_by", instrument, rng)
            explain = (f"{instrument} measures {correct}. An instrument is normally named after "
                       f"the quantity it reads, which is the quickest way to check an answer.")
            latex = None
        elif depth == 2:
            if rng.random() < 0.5:
                key = rng.choice(["a battery", "a mains outlet"])
                stem = f"What kind of current does {key} supply?"
                spec = {"kind": "fact", "table": "current_type", "key": key}
                correct, wrong = _fact_options("current_type", key, rng)
                explain = (f"{key.capitalize()} supplies {correct}. A battery drives current one "
                           f"way only, while a mains supply reverses direction periodically.")
            else:
                key = rng.choice(["a battery", "a generator", "a solar cell", "a thermocouple"])
                stem = f"Electricity from {key} is produced by which action?"
                spec = {"kind": "fact", "table": "actions", "key": key}
                correct, wrong = _fact_options("actions", key, rng)
                explain = (f"In {key} the electricity comes from {correct}. Each kind of source "
                           f"converts a different form of energy into electrical energy.")
            latex = None
        else:
            peak, r = rng.choice([100, 200, 240, 340]), rng.choice([50, 100, 120])
            value = peak / math.sqrt(2) / r
            stem = (f"An AC source is described by $V(t) = {peak}\\sin(\\omega t)$ volts and is "
                    f"connected across a {r} Ω resistor. What is the RMS current, to 2 decimal "
                    f"places?")
            spec = {"kind": "compute", "vars": {"p": peak, "r": r},
                    "expr": "p/sqrt(2)/r", "digits": 2}
            explain = (f"{peak} V is the peak value. The RMS voltage is ${peak}/\\sqrt2 = "
                       f"{fmt(peak / math.sqrt(2))}$ V, and dividing by {r} Ω gives "
                       f"{fmt(value)} A. RMS is the value that produces the same heating as an "
                       f"equal direct current.")
            latex = rf"I_{{rms}} = \frac{{{peak}/\sqrt2}}{{{r}}} = {fmt(value)}"
            correct, wrong = build(value, " A", [
                (peak / r, "Treats the peak voltage as the RMS value.", "missing-step"),
                (peak * math.sqrt(2) / r, "Multiplies by root two instead of dividing.", "inverted-operation"),
                (peak / 2 / r, "Halves the peak instead of dividing by root two.", "wrong-rule"),
                (r / (peak / math.sqrt(2)), "Inverts Ohm's law.", "inverted-operation")])

    return stem, correct, explain, wrong, spec, latex


# Reviewed once here rather than asserted per question, so the conceptual
# questions above are checkable rather than merely author-asserted.
# validation.py reads the same tables and recomputes the key from them.
#
# `answers` maps what the question asks about to its correct option. `pool` is
# every option that belongs in that question's category, and distractors are
# drawn only from it. That separation matters: a pool of mixed categories lets
# a student eliminate options by grammar instead of physics, which teaches
# nothing. The real paper keeps all four options in one category -- four units,
# or four instruments, or four kinds of current -- and so does this.
FACTS = {
    "si_units": {
        "answers": {
            "electric charge": "coulomb (C)",
            "current": "ampere (A)",
            "potential difference": "volt (V)",
            "resistance": "ohm (Ω)",
            "conductance": "siemens (S)",
            "capacitance": "farad (F)",
            "inductance": "henry (H)",
            "electrical power": "watt (W)",
            "electrical work": "joule (J)",
            "frequency": "hertz (Hz)",
        },
        "pool": ["coulomb (C)", "ampere (A)", "volt (V)", "ohm (Ω)", "siemens (S)",
                 "farad (F)", "henry (H)", "watt (W)", "joule (J)", "hertz (Hz)"],
        "why": "That is the unit of a different quantity.",
    },
    "measured_by": {
        "answers": {
            "An ammeter": "current",
            "A voltmeter": "potential difference",
            "An ohmmeter": "resistance",
            "A wattmeter": "electrical power",
        },
        "pool": ["current", "potential difference", "resistance", "electrical power",
                 "capacitance", "frequency", "charge"],
        "why": "That instrument reads a different quantity.",
    },
    "current_type": {
        "answers": {
            "a battery": "direct current (DC)",
            "a mains outlet": "alternating current (AC)",
        },
        "pool": ["direct current (DC)", "alternating current (AC)", "pulsating current",
                 "static charge", "no current at all"],
        "why": "That is not how this source behaves.",
    },
    "actions": {
        "answers": {
            "a battery": "a chemical action",
            "a generator": "a mechanical action",
            "a solar cell": "light falling on a semiconductor",
            "a thermocouple": "a difference in temperature",
        },
        "pool": ["a chemical action", "a mechanical action", "a magnetic action",
                 "light falling on a semiconductor", "a difference in temperature",
                 "a frictional action"],
        "why": "A different kind of source works this way.",
    },
}


def _fact_options(table, key, rng):
    """Correct entry plus distractors drawn from the same category pool.

    Every distractor is the right answer to a neighbouring question, so it is
    plausible, and taking them from one category means none can be eliminated
    on grammar alone.
    """
    entry = FACTS[table]
    correct = entry["answers"][key]
    others = [v for v in entry["pool"] if v != correct]
    rng.shuffle(others)
    return correct, [(v, entry["why"], "wrong-pairing") for v in others[:5]]
