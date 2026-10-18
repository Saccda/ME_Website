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


# Taking g as 9.8 and stating it in every stem, because the examination states
# it and a student should never have to guess which value was intended.
G = 9.8


def template(domain, depth, rng):
    """Return stem, answer, explanation, distractors, validator spec and LaTeX."""
    if domain == "kinematics":
        if depth == 0:
            d, t = rng.choice([120, 240, 360, 480]), rng.choice([8, 10, 12, 20])
            value = d / t
            stem = f"A trolley travels {d} m in {t} s at a steady speed. What is its speed?"
            spec = {"kind": "compute", "vars": {"d": d, "t": t}, "expr": "d/t", "digits": 2}
            explain = f"Speed is distance divided by time: ${d} \\div {t} = {fmt(value)}$ m/s."
            latex = rf"v = \frac{{s}}{{t}} = \frac{{{d}}}{{{t}}} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (t / d, "Divides time by distance.", "inverted-operation"),
                (d * t, "Multiplies instead of dividing.", "wrong-operation"),
                (d - t, "Subtracts the time from the distance.", "wrong-operation"),
                (d / t / 60, "Converts to a per-minute figure the question did not ask for.", "unit-error")])
        elif depth == 1:
            u, v, t = rng.choice([0, 2, 5]), rng.choice([12, 20, 30]), rng.choice([4, 5, 8])
            value = (v - u) / t
            stem = (f"A vehicle speeds up uniformly from {u} m/s to {v} m/s in {t} s. "
                    f"What is its acceleration?")
            spec = {"kind": "compute", "vars": {"u": u, "v": v, "t": t},
                    "expr": "(v-u)/t", "digits": 2}
            explain = (f"Acceleration is the change in velocity per second: "
                       f"$({v} - {u}) \\div {t} = {fmt(value)}$ m/s².")
            latex = rf"a = \frac{{v - u}}{{t}} = \frac{{{v} - {u}}}{{{t}}} = {fmt(value)}"
            correct, wrong = build(value, " m/s²", [
                ((v + u) / t, "Adds the two speeds instead of taking the change.", "wrong-operation"),
                (v / t, "Ignores the starting speed.", "missing-step"),
                ((v - u) * t, "Multiplies by the time instead of dividing.", "inverted-operation"),
                (t / (v - u) if v != u else v, "Divides time by the change in speed.", "inverted-operation")])
        elif depth == 2:
            u, a, t = rng.choice([0, 3, 5]), rng.choice([2, 3, 4]), rng.choice([4, 5, 6])
            value = u * t + 0.5 * a * t ** 2
            stem = (f"A body starts at {u} m/s and accelerates uniformly at {a} m/s² for {t} s. "
                    f"How far does it travel?")
            spec = {"kind": "compute", "vars": {"u": u, "a": a, "t": t},
                    "expr": "u*t+0.5*a*t**2", "digits": 2}
            explain = (f"$s = ut + \\tfrac12 at^2 = ({u})({t}) + 0.5({a})({t})^2 = "
                       f"{fmt(value)}$ m. Both terms are needed: the distance it would have "
                       f"covered at its starting speed, plus the extra from speeding up.")
            latex = rf"s = ut + \tfrac12 at^2 = {u}({t}) + \tfrac12({a})({t})^2 = {fmt(value)}"
            correct, wrong = build(value, " m", [
                (u * t, "Uses the starting speed only and ignores the acceleration.", "missing-step"),
                (0.5 * a * t ** 2, "Ignores the starting speed.", "missing-step"),
                (u * t + a * t ** 2, "Omits the factor of one half.", "missing-step"),
                ((u + a * t) * t, "Multiplies the final speed by the time, which overstates the distance.", "wrong-rule")])
        else:
            h = rng.choice([20, 45, 80, 125])
            value = math.sqrt(2 * G * h)
            stem = (f"A stone is dropped from rest from a height of {h} m. Neglecting air "
                    f"resistance and taking $g = {G}$ m/s², at what speed does it reach the "
                    f"ground, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"h": h, "g": G},
                    "expr": "sqrt(2*g*h)", "digits": 2}
            explain = (f"With $u = 0$, $v^2 = 2gh$, so $v = \\sqrt{{2({G})({h})}} = "
                       f"{fmt(value)}$ m/s. The mass does not appear: everything falls at the "
                       f"same rate once air resistance is ignored.")
            latex = rf"v = \sqrt{{2gh}} = \sqrt{{2({G})({h})}} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (math.sqrt(G * h), "Omits the factor of two.", "missing-step"),
                (2 * G * h, "Forgets to take the square root.", "missing-step"),
                (math.sqrt(2 * h / G), "Divides by g instead of multiplying.", "inverted-operation"),
                (G * h, "Multiplies g by the height and stops.", "missing-step")])

    elif domain == "forces":
        if depth == 0:
            m, a = rng.choice([2, 4, 5, 8]), rng.choice([3, 5, 6, 10])
            value = m * a
            stem = (f"A force gives {_a(m)} {m} kg mass an acceleration of {a} m/s². "
                    f"How large is the force?")
            spec = {"kind": "compute", "vars": {"m": m, "a": a}, "expr": "m*a", "digits": 2}
            explain = f"Newton's second law: $F = ma = {m} \\times {a} = {fmt(value)}$ N."
            latex = rf"F = ma = {m} \times {a} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (m / a, "Divides mass by acceleration.", "inverted-operation"),
                (a / m, "Divides acceleration by mass.", "inverted-operation"),
                (m + a, "Adds the two quantities.", "wrong-operation"),
                (m * a * G, "Multiplies by g, which belongs to weight, not to this force.", "wrong-rule")])
        elif depth == 1:
            m = rng.choice([5, 12, 20, 50])
            value = m * G
            stem = (f"What is the weight of {_a(m)} {m} kg component on Earth, "
                    f"taking $g = {G}$ m/s²?")
            spec = {"kind": "compute", "vars": {"m": m, "g": G}, "expr": "m*g", "digits": 2}
            explain = (f"Weight is the force gravity exerts: $W = mg = {m} \\times {G} = "
                       f"{fmt(value)}$ N. Mass is in kilograms; weight is a force in newtons.")
            latex = rf"W = mg = {m} \times {G} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (m, "Reports the mass, which is not a force.", "unit-error"),
                (m / G, "Divides by g instead of multiplying.", "inverted-operation"),
                (m * G * 2, "The result is doubled.", "arithmetic-slip"),
                (m + G, "Adds g to the mass.", "wrong-operation")])
        elif depth == 2:
            mu, m = rng.choice([0.2, 0.3, 0.4, 0.5]), rng.choice([10, 20, 25, 40])
            value = mu * m * G
            stem = (f"{_a(m).capitalize()} {m} kg crate rests on a level floor, and the coefficient of friction "
                    f"between them is {fmt(mu)}. What horizontal force is needed to start it "
                    f"sliding? Take $g = {G}$ m/s².")
            spec = {"kind": "compute", "vars": {"u": mu, "m": m, "g": G},
                    "expr": "u*m*g", "digits": 2}
            explain = (f"The normal force is the weight, $mg = {fmt(m * G)}$ N, and friction is "
                       f"$\\mu$ times it: ${fmt(mu)} \\times {fmt(m * G)} = {fmt(value)}$ N.")
            latex = rf"F = \mu mg = {fmt(mu)} \times {m} \times {G} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (m * G, "Gives the weight and ignores the coefficient.", "missing-step"),
                (mu * m, "Omits g, so this is not a force.", "missing-step"),
                (m * G / mu, "Divides by the coefficient instead of multiplying.", "inverted-operation"),
                (mu * G, "Leaves the mass out.", "missing-step")])
        else:
            f, mu, m = rng.choice([200, 300, 400]), rng.choice([0.2, 0.25]), rng.choice([20, 25, 30])
            friction = mu * m * G
            value = (f - friction) / m
            stem = (f"A horizontal force of {f} N is applied to {_a(m)} {m} kg box on a floor whose "
                    f"coefficient of friction is {fmt(mu)}. What is the box's acceleration, to "
                    f"2 decimal places? Take $g = {G}$ m/s².")
            spec = {"kind": "compute", "vars": {"f": f, "u": mu, "m": m, "g": G},
                    "expr": "(f-u*m*g)/m", "digits": 2}
            explain = (f"Friction opposes the push: ${fmt(mu)} \\times {m} \\times {G} = "
                       f"{fmt(friction)}$ N. The resultant force is ${f} - {fmt(friction)} = "
                       f"{fmt(f - friction)}$ N, and dividing by the mass gives {fmt(value)} m/s².")
            latex = rf"a = \frac{{F - \mu mg}}{{m}} = \frac{{{f} - {fmt(friction)}}}{{{m}}} = {fmt(value)}"
            correct, wrong = build(value, " m/s²", [
                (f / m, "Ignores friction entirely.", "missing-step"),
                ((f + friction) / m, "Adds friction instead of subtracting it.", "sign-error"),
                (f - friction, "Gives the resultant force, not the acceleration.", "partial-answer"),
                (friction / m, "Uses only the friction force.", "wrong-term")])

    elif domain == "energy":
        if depth == 0:
            f, d = rng.choice([20, 50, 80, 120]), rng.choice([3, 5, 8, 10])
            value = f * d
            stem = (f"A force of {f} N moves a load {d} m in the direction of the force. "
                    f"How much work is done?")
            spec = {"kind": "compute", "vars": {"f": f, "d": d}, "expr": "f*d", "digits": 2}
            explain = f"Work is force times distance moved: ${f} \\times {d} = {fmt(value)}$ J."
            latex = rf"W = Fd = {f} \times {d} = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (f / d, "Divides instead of multiplying.", "inverted-operation"),
                (d / f, "Divides distance by force.", "inverted-operation"),
                (f + d, "Adds the two quantities.", "wrong-operation"),
                (f * d / 2, "Halves the result.", "arithmetic-slip")])
        elif depth == 1:
            m, v = rng.choice([2, 4, 10, 20]), rng.choice([3, 5, 6, 10])
            value = 0.5 * m * v ** 2
            stem = f"What is the kinetic energy of {_a(m)} {m} kg mass moving at {v} m/s?"
            spec = {"kind": "compute", "vars": {"m": m, "v": v},
                    "expr": "0.5*m*v**2", "digits": 2}
            explain = (f"$E_k = \\tfrac12 mv^2 = 0.5 \\times {m} \\times {v}^2 = {fmt(value)}$ J. "
                       f"The speed is squared, so doubling it quadruples the energy.")
            latex = rf"E_k = \tfrac12 mv^2 = 0.5 \times {m} \times {v}^2 = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (m * v ** 2, "Omits the factor of one half.", "missing-step"),
                (0.5 * m * v, "Omits the square on the speed.", "missing-step"),
                (m * v, "Gives the momentum instead of the energy.", "wrong-rule"),
                (0.5 * m ** 2 * v, "Squares the mass instead of the speed.", "wrong-term")])
        elif depth == 2:
            m, h = rng.choice([5, 10, 20, 25]), rng.choice([2, 4, 6, 10])
            value = m * G * h
            stem = (f"How much potential energy does {_a(m)} {m} kg mass gain when it is raised "
                    f"{h} m? Take $g = {G}$ m/s².")
            spec = {"kind": "compute", "vars": {"m": m, "g": G, "h": h},
                    "expr": "m*g*h", "digits": 2}
            explain = f"$E_p = mgh = {m} \\times {G} \\times {h} = {fmt(value)}$ J."
            latex = rf"E_p = mgh = {m} \times {G} \times {h} = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (m * h, "Omits g.", "missing-step"),
                (m * G, "Gives the weight and ignores the height.", "partial-answer"),
                (m * G * h / 2, "Uses the factor of one half, which belongs to kinetic energy.", "wrong-rule"),
                (G * h, "Leaves the mass out.", "missing-step")])
        else:
            m, h, t = rng.choice([40, 60, 80]), rng.choice([5, 10, 12]), rng.choice([4, 8, 10])
            value = m * G * h / t
            stem = (f"A hoist raises {_a(m)} {m} kg load {h} m in {t} s. What is its output "
                    f"power, to 2 decimal places? Take $g = {G}$ m/s².")
            spec = {"kind": "compute", "vars": {"m": m, "g": G, "h": h, "t": t},
                    "expr": "m*g*h/t", "digits": 2}
            explain = (f"The work done is $mgh = {m} \\times {G} \\times {h} = {fmt(m * G * h)}$ J, "
                       f"and power is work per second: ${fmt(m * G * h)} \\div {t} = {fmt(value)}$ W.")
            latex = rf"P = \frac{{mgh}}{{t}} = \frac{{{m} \times {G} \times {h}}}{{{t}}} = {fmt(value)}"
            correct, wrong = build(value, " W", [
                (m * G * h, "Gives the work in joules, not the power.", "partial-answer"),
                (m * G * h * t, "Multiplies by the time instead of dividing.", "inverted-operation"),
                (m * h / t, "Omits g.", "missing-step"),
                (m * G / t, "Leaves the height out.", "missing-step")])

    elif domain == "fluids":
        if depth == 0:
            m, v = rng.choice([200, 400, 600, 800]), rng.choice([2, 4, 5, 8])
            value = m / v
            stem = f"A block of mass {m} kg occupies {v} m³. What is its density?"
            spec = {"kind": "compute", "vars": {"m": m, "v": v}, "expr": "m/v", "digits": 2}
            explain = f"Density is mass per unit volume: ${m} \\div {v} = {fmt(value)}$ kg/m³."
            latex = rf"\rho = \frac{{m}}{{V}} = \frac{{{m}}}{{{v}}} = {fmt(value)}"
            correct, wrong = build(value, " kg/m³", [
                (v / m, "Divides volume by mass.", "inverted-operation"),
                (m * v, "Multiplies instead of dividing.", "inverted-operation"),
                (m - v, "Subtracts the volume from the mass.", "wrong-operation"),
                (m / v / 1000, "Converts as though the answer were wanted in g/cm³.", "unit-error")])
        elif depth == 1:
            f, a = rng.choice([200, 450, 600, 900]), rng.choice([2, 3, 5, 6])
            value = f / a
            stem = f"A force of {f} N presses evenly on an area of {a} m². What is the pressure?"
            spec = {"kind": "compute", "vars": {"f": f, "a": a}, "expr": "f/a", "digits": 2}
            explain = (f"Pressure is force per unit area: ${f} \\div {a} = {fmt(value)}$ Pa. "
                       f"One pascal is one newton per square metre.")
            latex = rf"p = \frac{{F}}{{A}} = \frac{{{f}}}{{{a}}} = {fmt(value)}"
            correct, wrong = build(value, " Pa", [
                (a / f, "Divides area by force.", "inverted-operation"),
                (f * a, "Multiplies instead of dividing.", "inverted-operation"),
                (f + a, "Adds the two quantities.", "wrong-operation"),
                (f / a / 1000, "Reports kilopascals while the question asks for pascals.", "unit-error")])
        elif depth == 2:
            h = rng.choice([2, 5, 8, 12])
            value = 1000 * G * h
            stem = (f"What is the pressure due to a column of water {h} m deep? Take the density "
                    f"of water as 1000 kg/m³ and $g = {G}$ m/s².")
            spec = {"kind": "compute", "vars": {"r": 1000, "g": G, "h": h},
                    "expr": "r*g*h", "digits": 2}
            explain = (f"$p = \\rho gh = 1000 \\times {G} \\times {h} = {fmt(value)}$ Pa. The "
                       f"area does not appear: depth alone sets the pressure in a liquid.")
            latex = rf"p = \rho gh = 1000 \times {G} \times {h} = {fmt(value)}"
            correct, wrong = build(value, " Pa", [
                (1000 * h, "Omits g.", "missing-step"),
                (G * h, "Leaves the density out.", "missing-step"),
                (1000 * G / h, "Divides by the depth instead of multiplying.", "inverted-operation"),
                (1000 * G * h / 2, "Halves the result.", "arithmetic-slip")])
        else:
            v = rng.choice([0.002, 0.005, 0.01, 0.02])
            value = 1000 * v * G
            stem = (f"A solid of volume {fmt(v, 3)} m³ is fully submerged in water. What upthrust "
                    f"acts on it? Take the density of water as 1000 kg/m³ and $g = {G}$ m/s².")
            spec = {"kind": "compute", "vars": {"r": 1000, "v": v, "g": G},
                    "expr": "r*v*g", "digits": 2}
            explain = (f"The upthrust equals the weight of water displaced: the displaced mass is "
                       f"$1000 \\times {fmt(v, 3)} = {fmt(1000 * v)}$ kg, and its weight is "
                       f"${fmt(1000 * v)} \\times {G} = {fmt(value)}$ N.")
            latex = rf"F = \rho Vg = 1000 \times {fmt(v, 3)} \times {G} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (1000 * v, "Gives the displaced mass, not its weight.", "partial-answer"),
                (v * G, "Leaves the density out.", "missing-step"),
                (1000 * G / v, "Divides by the volume instead of multiplying.", "inverted-operation"),
                (1000 * v * G / 2, "Halves the result.", "arithmetic-slip")])

    elif domain == "thermal":
        if depth == 0:
            t = rng.choice([15, 27, 50, 100, 127])
            value = t + 273
            stem = f"A gas is at {t} °C. What is this temperature in kelvin?"
            spec = {"kind": "compute", "vars": {"t": t}, "expr": "t+273", "digits": 2}
            explain = (f"Add 273 to go from degrees Celsius to kelvin: ${t} + 273 = "
                       f"{fmt(value)}$ K. A kelvin is the same size as a degree Celsius; only "
                       f"the zero differs.")
            latex = rf"T = {t} + 273 = {fmt(value)}"
            correct, wrong = build(value, " K", [
                (t - 273, "Subtracts instead of adding.", "sign-error"),
                (273 - t, "Subtracts the temperature from 273.", "sign-error"),
                (t + 100, "Adds 100 instead of 273.", "wrong-constant"),
                (t * 273, "Multiplies by 273.", "wrong-operation")])
        elif depth == 1:
            m, dt = rng.choice([2, 4, 5]), rng.choice([10, 20, 25, 30])
            value = m * 4200 * dt
            stem = (f"How much heat is needed to raise the temperature of {m} kg of water by "
                    f"{dt} °C? Take the specific heat capacity of water as 4200 J/(kg·K).")
            spec = {"kind": "compute", "vars": {"m": m, "c": 4200, "d": dt},
                    "expr": "m*c*d", "digits": 2}
            explain = (f"$Q = mc\\Delta T = {m} \\times 4200 \\times {dt} = {fmt(value)}$ J.")
            latex = rf"Q = mc\Delta T = {m} \times 4200 \times {dt} = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (m * 4200, "Leaves the temperature rise out.", "missing-step"),
                (4200 * dt, "Leaves the mass out.", "missing-step"),
                (m * dt, "Omits the specific heat capacity.", "missing-step"),
                (m * 4200 * dt / 2, "Halves the result.", "arithmetic-slip")])
        elif depth == 2:
            m = rng.choice([0.5, 2, 3, 5])
            value = m * 334
            stem = (f"How much heat is needed to melt {fmt(m)} kg of ice already at 0 °C? Take "
                    f"the specific latent heat of fusion as 334 kJ/kg.")
            spec = {"kind": "compute", "vars": {"m": m, "l": 334}, "expr": "m*l", "digits": 2}
            explain = (f"$Q = mL = {fmt(m)} \\times 334 = {fmt(value)}$ kJ. The temperature does "
                       f"not change while it melts, so no $mc\\Delta T$ term appears.")
            latex = rf"Q = mL = {fmt(m)} \times 334 = {fmt(value)}"
            correct, wrong = build(value, " kJ", [
                (m / 334, "Divides instead of multiplying.", "inverted-operation"),
                (334 / m, "Divides the latent heat by the mass.", "inverted-operation"),
                (m + 334, "Adds the two quantities.", "wrong-operation"),
                (m * 4.2 * 334, "Brings in a specific heat term, which does not apply while melting.", "wrong-rule")])
        else:
            p1, v1, v2 = rng.choice([100, 150, 200]), rng.choice([4, 6, 8]), rng.choice([1, 2])
            value = p1 * v1 / v2
            stem = (f"A gas at {p1} kPa occupies {v1} m³. It is compressed to {v2} m³ at constant "
                    f"temperature. What is its new pressure?")
            spec = {"kind": "compute", "vars": {"p": p1, "a": v1, "b": v2},
                    "expr": "p*a/b", "digits": 2}
            explain = (f"At constant temperature $p_1V_1 = p_2V_2$, so $p_2 = "
                       f"\\frac{{{p1} \\times {v1}}}{{{v2}}} = {fmt(value)}$ kPa. Squeezing a gas "
                       f"into a smaller volume raises its pressure.")
            latex = rf"p_2 = \frac{{p_1 V_1}}{{V_2}} = \frac{{{p1} \times {v1}}}{{{v2}}} = {fmt(value)}"
            correct, wrong = build(value, " kPa", [
                (p1 * v2 / v1, "Inverts the volume ratio, giving a fall in pressure.", "inverted-operation"),
                (p1 * v1 * v2, "Multiplies by the new volume instead of dividing.", "inverted-operation"),
                (p1 / (v1 * v2), "Divides by both volumes.", "inverted-operation"),
                (p1 + v1 - v2, "Treats the relationship as additive.", "wrong-rule")])

    elif domain == "current":
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

    elif domain == "momentum":
        if depth == 0:
            m, v = rng.choice([2, 5, 8, 12]), rng.choice([4, 6, 15, 20])
            value = m * v
            stem = f"A trolley of mass {m} kg moves at {v} m/s. What is its momentum?"
            spec = {"kind": "compute", "vars": {"m": m, "v": v}, "expr": "m*v", "digits": 2}
            explain = (f"Momentum is mass times velocity: ${m} \\times {v} = {fmt(value)}$ kg·m/s. "
                       f"It is a vector, so its direction is the direction of travel.")
            latex = rf"p = mv = {m} \times {v} = {fmt(value)}"
            correct, wrong = build(value, " kg·m/s", [
                (0.5 * m * v ** 2, "Computes kinetic energy instead of momentum.", "wrong-rule"),
                (0.5 * m * v, "Carries a factor of one half that momentum does not have.", "wrong-rule"),
                (m / v, "Divides mass by velocity.", "inverted-operation"),
                (m + v, "Adds the two quantities.", "wrong-operation")])
        elif depth == 1:
            m, u, v = rng.choice([2, 4, 5]), rng.choice([3, 5, 8]), rng.choice([12, 15, 20])
            value = m * (v - u)
            stem = (f"A body of mass {m} kg speeds up from {u} m/s to {v} m/s. What impulse "
                    f"has acted on it?")
            spec = {"kind": "compute", "vars": {"m": m, "u": u, "v": v},
                    "expr": "m*(v-u)", "digits": 2}
            explain = (f"Impulse equals the change in momentum: ${m}({v} - {u}) = {fmt(value)}$ "
                       f"N·s. Only the change matters, not the speeds themselves.")
            latex = rf"J = m(v-u) = {m}({v} - {u}) = {fmt(value)}"
            correct, wrong = build(value, " N·s", [
                (m * (v + u), "Adds the speeds instead of taking the change.", "wrong-operation"),
                (m * v, "Uses the final speed only.", "missing-step"),
                (v - u, "Leaves the mass out.", "missing-step"),
                (m * u, "Uses the starting speed only.", "missing-step")])
        elif depth == 2:
            m1, u1, m2 = rng.choice([2, 3, 4]), rng.choice([4, 6, 8]), rng.choice([1, 2, 6])
            value = m1 * u1 / (m1 + m2)
            stem = (f"A {m1} kg trolley moving at {u1} m/s strikes a stationary {m2} kg trolley "
                    f"and the two move off locked together. What is their common speed?")
            spec = {"kind": "compute", "vars": {"m1": m1, "u1": u1, "m2": m2},
                    "expr": "m1*u1/(m1+m2)", "digits": 2}
            explain = (f"Momentum is conserved: ${m1} \\times {u1} = ({m1} + {m2})v$, so "
                       f"$v = {fmt(value)}$ m/s. Kinetic energy is not conserved here — the "
                       f"collision is inelastic — but momentum always is.")
            latex = rf"v = \frac{{m_1u_1}}{{m_1+m_2}} = \frac{{{m1}({u1})}}{{{m1+m2}}} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (u1, "Assumes the moving trolley keeps its speed.", "missing-step"),
                (m1 * u1 / m2, "Divides by the struck mass alone.", "wrong-rule"),
                (u1 / 2, "Halves the speed regardless of the two masses.", "wrong-rule"),
                (m1 * u1, "Stops at the momentum without dividing by the total mass.", "missing-step")])
        else:
            m, mb, v = rng.choice([4, 5, 8]), rng.choice([10, 20, 40]), rng.choice([300, 400, 500])
            value = mb / 1000 * v / m
            stem = (f"A rifle of mass {m} kg fires a {mb} g bullet at {v} m/s. What is the "
                    f"recoil speed of the rifle, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"m": m, "mb": mb, "v": v},
                    "expr": "mb/1000*v/m", "digits": 2}
            explain = (f"The pair starts at rest, so the momenta are equal and opposite: "
                       f"$({mb}/1000)({v}) = {m}v_r$, giving $v_r = {fmt(value)}$ m/s. The bullet "
                       f"mass must be converted to kilograms first.")
            latex = rf"v_r = \frac{{m_bv_b}}{{m}} = \frac{{{mb / 1000:g}({v})}}{{{m}}} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (mb * v / m, "Leaves the bullet mass in grams.", "unit-error"),
                (v / m, "Omits the bullet mass entirely.", "missing-step"),
                (m * v / (mb / 1000), "Inverts the mass ratio.", "inverted-operation"),
                (mb / 1000 * v, "Stops at the bullet's momentum.", "missing-step")])

    elif domain == "rotation":
        if depth == 0:
            v, r = rng.choice([6, 10, 12, 20]), rng.choice([4, 5, 8, 10])
            value = v ** 2 / r
            stem = (f"A car rounds a bend of radius {r} m at a steady {v} m/s. What is its "
                    f"centripetal acceleration?")
            spec = {"kind": "compute", "vars": {"v": v, "r": r}, "expr": "v**2/r", "digits": 2}
            explain = (f"$a_c = v^2/r = {v}^2 \\div {r} = {fmt(value)}$ m/s². The speed is "
                       f"squared, so doubling it quadruples the acceleration.")
            latex = rf"a_c = \frac{{v^2}}{{r}} = \frac{{{v}^2}}{{{r}}} = {fmt(value)}"
            correct, wrong = build(value, " m/s²", [
                (v / r, "Does not square the speed.", "missing-step"),
                (v ** 2 * r, "Multiplies by the radius instead of dividing.", "inverted-operation"),
                (r / v ** 2, "Inverts the whole expression.", "inverted-operation"),
                (2 * v / r, "Doubles the speed rather than squaring it.", "wrong-rule")])
        elif depth == 1:
            w, t = rng.choice([10, 20, 25, 40]), rng.choice([30, 60, 120])
            value = w * t / (2 * math.pi)
            stem = (f"A wheel turns at a steady {w} rad/s. How many complete revolutions does it "
                    f"make in {t} s, to the nearest revolution?")
            spec = {"kind": "compute", "vars": {"w": w, "t": t}, "expr": "w*t/(2*pi)", "digits": 0}
            explain = (f"It sweeps ${w} \\times {t} = {w * t}$ radians, and one revolution is "
                       f"$2\\pi$ radians, so that is ${w * t} \\div 2\\pi \\approx "
                       f"{fmt(value, 0)}$ revolutions.")
            latex = rf"N = \frac{{\omega t}}{{2\pi}} = \frac{{{w}({t})}}{{2\pi}} \approx {fmt(value, 0)}"
            correct, wrong = build(value, " rev", [
                (w * t, "Leaves the answer in radians.", "unit-error"),
                (w * t / math.pi, "Divides by pi rather than two pi.", "wrong-rule"),
                (w * t * 2 * math.pi, "Multiplies by two pi instead of dividing.", "inverted-operation"),
                (w / t, "Divides the angular speed by the time.", "inverted-operation")], digits=0)
        elif depth == 2:
            inertia, alpha = rng.choice([2, 4, 6, 10]), rng.choice([3, 5, 8, 12])
            value = inertia * alpha
            stem = (f"A flywheel of moment of inertia {inertia} kg·m² is given an angular "
                    f"acceleration of {alpha} rad/s². What net torque acts on it?")
            spec = {"kind": "compute", "vars": {"i": inertia, "al": alpha},
                    "expr": "i*al", "digits": 2}
            explain = (f"Torque is the rotational form of $F = ma$: $\\tau = I\\alpha = "
                       f"{inertia} \\times {alpha} = {fmt(value)}$ N·m.")
            latex = rf"\tau = I\alpha = {inertia} \times {alpha} = {fmt(value)}"
            correct, wrong = build(value, " N·m", [
                (inertia / alpha, "Divides the inertia by the acceleration.", "inverted-operation"),
                (alpha / inertia, "Inverts the relationship.", "inverted-operation"),
                (0.5 * inertia * alpha, "Introduces a factor of one half.", "wrong-rule"),
                (inertia + alpha, "Adds the two quantities.", "wrong-operation")])
        else:
            inertia, w = rng.choice([2, 4, 5, 8]), rng.choice([6, 10, 12, 20])
            value = 0.5 * inertia * w ** 2
            stem = (f"A flywheel of moment of inertia {inertia} kg·m² spins at {w} rad/s. What is "
                    f"its rotational kinetic energy?")
            spec = {"kind": "compute", "vars": {"i": inertia, "w": w},
                    "expr": "0.5*i*w**2", "digits": 2}
            explain = (f"$E_r = \\tfrac12 I\\omega^2 = 0.5 \\times {inertia} \\times {w}^2 = "
                       f"{fmt(value)}$ J. It mirrors $\\tfrac12 mv^2$, with inertia for mass and "
                       f"angular speed for speed.")
            latex = rf"E_r = \tfrac12 I\omega^2 = \tfrac12({inertia})({w})^2 = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (inertia * w ** 2, "Omits the factor of one half.", "missing-step"),
                (0.5 * inertia * w, "Does not square the angular speed.", "missing-step"),
                (0.5 * inertia ** 2 * w, "Squares the inertia instead of the angular speed.", "wrong-rule"),
                (inertia * w, "Gives angular momentum rather than energy.", "wrong-rule")])

    elif domain == "thermo":
        if depth == 0:
            process = rng.choice(["an isothermal process", "an isochoric process",
                                  "an isobaric process"])
            stem = f"In {process}, which quantity stays constant?"
            spec = {"kind": "fact", "table": "constant_in_process", "key": process}
            correct, wrong = _fact_options("constant_in_process", process, rng)
            explain = (f"In {process} it is {correct} that is held constant. The name says which: "
                       f"iso-thermal fixes temperature, iso-choric fixes volume, iso-baric fixes "
                       f"pressure.")
            latex = None
        elif depth == 1:
            heat, work = rng.choice([300, 500, 800, 1200]), rng.choice([100, 200, 450])
            value = heat - work
            stem = (f"A system absorbs {heat} J of heat and does {work} J of work on its "
                    f"surroundings. What is the change in its internal energy?")
            spec = {"kind": "compute", "vars": {"q": heat, "w": work}, "expr": "q-w", "digits": 2}
            explain = (f"The first law is $\\Delta U = Q - W$: ${heat} - {work} = {fmt(value)}$ J. "
                       f"Heat in raises the internal energy, work done by the system lowers it.")
            latex = rf"\Delta U = Q - W = {heat} - {work} = {fmt(value)}"
            correct, wrong = build(value, " J", [
                (heat + work, "Adds the work instead of subtracting it.", "sign-error"),
                (work - heat, "Reverses the subtraction.", "sign-error"),
                (heat, "Ignores the work done.", "missing-step"),
                (work, "Reports the work rather than the change in internal energy.", "wrong-rule")])
        elif depth == 2:
            hot = rng.choice([800, 1000, 1500, 2000])
            cold = rng.choice([200, 300, 450, 600])
            value = (hot - cold) / hot * 100
            stem = (f"A heat engine takes in {hot} J from its hot reservoir and rejects {cold} J "
                    f"to the cold one. What is its efficiency, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"h": hot, "c": cold},
                    "expr": "(h-c)/h*100", "digits": 2}
            explain = (f"Efficiency is useful work over heat supplied: $({hot} - {cold}) \\div "
                       f"{hot} = {fmt(value / 100, 4)}$, which is {fmt(value)}%. The rejected heat "
                       f"is the part that does no work.")
            latex = rf"e = \frac{{Q_H - Q_C}}{{Q_H}} = \frac{{{hot} - {cold}}}{{{hot}}} = {fmt(value)}\%"
            correct, wrong = build(value, "%", [
                (cold / hot * 100, "Reports the fraction rejected rather than the fraction used.", "wrong-rule"),
                (hot / cold * 100, "Inverts the ratio and exceeds 100%.", "inverted-operation"),
                ((hot - cold) / cold * 100, "Divides by the rejected heat.", "wrong-rule"),
                (hot - cold, "Gives the work in joules, not an efficiency.", "unit-error")])
        else:
            hot_c = rng.choice([227, 327, 427, 527])
            cold_c = rng.choice([27, 77, 127])
            value = (1 - (cold_c + 273.15) / (hot_c + 273.15)) * 100
            stem = (f"A Carnot engine works between reservoirs at {hot_c} °C and {cold_c} °C. "
                    f"What is the greatest efficiency it can reach, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"h": hot_c, "c": cold_c},
                    "expr": "(1-(c+273.15)/(h+273.15))*100", "digits": 2}
            explain = (f"Carnot efficiency is $1 - T_C/T_H$ with both temperatures in kelvin: "
                       f"$1 - {cold_c + 273.15:g}/{hot_c + 273.15:g} = {fmt(value / 100, 4)}$, or "
                       f"{fmt(value)}%. Using Celsius here is the usual mistake.")
            latex = (rf"e = 1 - \frac{{T_C}}{{T_H}} = 1 - \frac{{{cold_c + 273.15:g}}}"
                     rf"{{{hot_c + 273.15:g}}} = {fmt(value)}\%")
            correct, wrong = build(value, "%", [
                ((1 - cold_c / hot_c) * 100, "Uses Celsius instead of kelvin.", "unit-error"),
                ((1 - (hot_c + 273.15) / (cold_c + 273.15)) * 100, "Inverts the temperature ratio.", "inverted-operation"),
                ((cold_c + 273.15) / (hot_c + 273.15) * 100, "Gives the ratio itself rather than one minus it.", "missing-step"),
                (hot_c - cold_c, "Reports the temperature difference as a percentage.", "wrong-rule")])

    elif domain == "flow":
        if depth == 0:
            v, d1, d2 = rng.choice([2, 3, 4]), rng.choice([10, 12, 20]), rng.choice([5, 6, 4])
            value = v * (d1 / d2) ** 2
            stem = (f"Water flows at {v} m/s through a pipe of internal diameter {d1} cm. What is "
                    f"its speed where the pipe narrows to {d2} cm?")
            spec = {"kind": "compute", "vars": {"v": v, "d1": d1, "d2": d2},
                    "expr": "v*(d1/d2)**2", "digits": 2}
            explain = (f"Continuity gives $A_1v_1 = A_2v_2$, and area goes with the square of the "
                       f"diameter, so $v_2 = {v}({d1}/{d2})^2 = {fmt(value)}$ m/s. Halving the "
                       f"diameter quadruples the speed.")
            latex = rf"v_2 = v_1\left(\frac{{d_1}}{{d_2}}\right)^2 = {v}\left(\frac{{{d1}}}{{{d2}}}\right)^2 = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (v * d1 / d2, "Scales with diameter rather than with area.", "missing-step"),
                (v * (d2 / d1) ** 2, "Inverts the diameter ratio.", "inverted-operation"),
                (v * d2 / d1, "Inverts the ratio and omits the square.", "inverted-operation"),
                (v, "Assumes the speed is unchanged.", "no-change")])
        elif depth == 1:
            force, a1, a2 = rng.choice([50, 100, 200]), rng.choice([0.01, 0.02]), rng.choice([0.2, 0.5])
            value = force * a2 / a1
            stem = (f"In a hydraulic press a force of {force} N is applied to a piston of area "
                    f"{a1:g} m². What force appears on a piston of area {a2:g} m²?")
            spec = {"kind": "compute", "vars": {"f": force, "a1": a1, "a2": a2},
                    "expr": "f*a2/a1", "digits": 2}
            explain = (f"Pascal's principle makes the pressure equal on both pistons, so "
                       f"$F_2 = F_1 A_2/A_1 = {force} \\times {a2:g}/{a1:g} = {fmt(value)}$ N. "
                       f"The force is multiplied by the area ratio, not by distance.")
            latex = rf"F_2 = F_1\frac{{A_2}}{{A_1}} = {force}\frac{{{a2:g}}}{{{a1:g}}} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (force * a1 / a2, "Inverts the area ratio and reduces the force.", "inverted-operation"),
                (force, "Assumes the force passes through unchanged.", "no-change"),
                (force * a2, "Multiplies by the output area without dividing by the input.", "missing-step"),
                (force / a1, "Gives the pressure rather than the output force.", "wrong-rule")])
        elif depth == 2:
            h = rng.choice([1.25, 2, 3.2, 5])
            value = math.sqrt(2 * G * h)
            stem = (f"Water escapes through a small hole {h:g} m below the surface of a large "
                    f"open tank. Taking $g = {G}$ m/s², what is the efflux speed, to 2 decimal "
                    f"places?")
            spec = {"kind": "compute", "vars": {"h": h, "g": G},
                    "expr": "sqrt(2*g*h)", "digits": 2}
            explain = (f"Torricelli's law follows from Bernoulli: $v = \\sqrt{{2gh}} = "
                       f"\\sqrt{{2({G})({h:g})}} = {fmt(value)}$ m/s — the speed a body would "
                       f"reach falling that same height.")
            latex = rf"v = \sqrt{{2gh}} = \sqrt{{2({G})({h:g})}} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (2 * G * h, "Forgets the square root.", "missing-step"),
                (math.sqrt(G * h), "Omits the factor of two.", "missing-step"),
                (math.sqrt(2 * h / G), "Divides by g instead of multiplying.", "inverted-operation"),
                (G * h, "Multiplies g by the depth and stops.", "missing-step")])
        else:
            rho, v, dia = rng.choice([1000, 800]), rng.choice([1, 2, 3]), rng.choice([0.05, 0.1, 0.2])
            eta = rng.choice([0.001, 0.002])
            value = rho * v * dia / eta
            stem = (f"A fluid of density {rho} kg/m³ and dynamic viscosity {eta:g} Pa·s flows at "
                    f"{v} m/s through a pipe of diameter {dia:g} m. What is the Reynolds number?")
            spec = {"kind": "compute", "vars": {"rho": rho, "v": v, "d": dia, "eta": eta},
                    "expr": "rho*v*d/eta", "digits": 0}
            explain = (f"$Re = \\rho v D/\\eta = ({rho})({v})({dia:g})/{eta:g} = {fmt(value, 0)}$. "
                       f"It is dimensionless, and above roughly 4000 the flow is turbulent.")
            latex = rf"Re = \frac{{\rho v D}}{{\eta}} = \frac{{({rho})({v})({dia:g})}}{{{eta:g}}} = {fmt(value, 0)}"
            correct, wrong = build(value, "", [
                (eta / (rho * v * dia), "Inverts the whole expression.", "inverted-operation"),
                (rho * v / (dia * eta), "Divides by the diameter instead of multiplying.", "inverted-operation"),
                (rho * v * dia, "Leaves the viscosity out.", "missing-step"),
                (v * dia / eta, "Leaves the density out.", "missing-step")], digits=0)

    elif domain == "waves":
        if depth == 0:
            f, lam = rng.choice([50, 170, 250, 400]), rng.choice([0.8, 2, 4, 1.5])
            value = f * lam
            stem = (f"A wave has a frequency of {f} Hz and a wavelength of {lam:g} m. What is "
                    f"its speed?")
            spec = {"kind": "compute", "vars": {"f": f, "l": lam}, "expr": "f*l", "digits": 2}
            explain = (f"$v = f\\lambda = {f} \\times {lam:g} = {fmt(value)}$ m/s. Each cycle "
                       f"advances the wave by one wavelength, and there are {f} of them a second.")
            latex = rf"v = f\lambda = {f} \times {lam:g} = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (f / lam, "Divides frequency by wavelength.", "inverted-operation"),
                (lam / f, "Inverts the relationship.", "inverted-operation"),
                (f + lam, "Adds the two quantities.", "wrong-operation"),
                (1 / (f * lam), "Takes the reciprocal of the product.", "inverted-operation")])
        elif depth == 1:
            length = rng.choice([0.25, 0.5, 1.0, 2.0])
            value = 2 * math.pi * math.sqrt(length / G)
            stem = (f"A simple pendulum is {length:g} m long. Taking $g = {G}$ m/s², what is its "
                    f"period, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"l": length, "g": G},
                    "expr": "2*pi*sqrt(l/g)", "digits": 2}
            explain = (f"$T = 2\\pi\\sqrt{{L/g}} = 2\\pi\\sqrt{{{length:g}/{G}}} = {fmt(value)}$ s. "
                       f"The mass of the bob does not appear, and the length is under the root, so "
                       f"quadrupling it only doubles the period.")
            latex = rf"T = 2\pi\sqrt{{\frac{{L}}{{g}}}} = 2\pi\sqrt{{\frac{{{length:g}}}{{{G}}}}} = {fmt(value)}"
            correct, wrong = build(value, " s", [
                (2 * math.pi * math.sqrt(G / length), "Inverts the fraction under the root.", "inverted-operation"),
                (2 * math.pi * length / G, "Omits the square root.", "missing-step"),
                (math.sqrt(length / G), "Leaves out the factor of two pi.", "missing-step"),
                (1 / (2 * math.pi * math.sqrt(length / G)), "Gives the frequency instead of the period.", "wrong-rule")])
        elif depth == 2:
            amp, f = rng.choice([0.02, 0.05, 0.1, 0.2]), rng.choice([2, 5, 10])
            value = amp * 2 * math.pi * f
            stem = (f"A body in simple harmonic motion has an amplitude of {amp:g} m and a "
                    f"frequency of {f} Hz. What is its maximum speed, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"a": amp, "f": f},
                    "expr": "a*2*pi*f", "digits": 2}
            explain = (f"$v_{{max}} = A\\omega$ and $\\omega = 2\\pi f$, so $v_{{max}} = "
                       f"{amp:g} \\times 2\\pi \\times {f} = {fmt(value)}$ m/s. It occurs as the "
                       f"body passes through the centre, where the acceleration is zero.")
            latex = rf"v_{{max}} = A\omega = {amp:g}(2\pi \times {f}) = {fmt(value)}"
            correct, wrong = build(value, " m/s", [
                (amp * f, "Uses the frequency in place of the angular frequency.", "missing-step"),
                (amp * (2 * math.pi * f) ** 2, "Gives the maximum acceleration instead.", "wrong-rule"),
                (2 * math.pi * f / amp, "Divides by the amplitude.", "inverted-operation"),
                (amp / (2 * math.pi * f), "Inverts the relationship.", "inverted-operation")])
        else:
            length, v, n = rng.choice([0.5, 1.0, 2.0]), rng.choice([100, 200, 340]), rng.choice([2, 3, 4])
            value = n * v / (2 * length)
            stem = (f"A string of length {length:g} m is fixed at both ends and carries waves at "
                    f"{v} m/s. What is the frequency of its harmonic number {n}?")
            spec = {"kind": "compute", "vars": {"n": n, "v": v, "l": length},
                    "expr": "n*v/(2*l)", "digits": 2}
            explain = (f"$f_n = nv/2L = {n}({v}) \\div (2 \\times {length:g}) = {fmt(value)}$ Hz. "
                       f"The fundamental fits half a wavelength on the string, and harmonic $n$ "
                       f"fits $n$ of those halves.")
            latex = rf"f_n = \frac{{nv}}{{2L}} = \frac{{{n}({v})}}{{2({length:g})}} = {fmt(value)}"
            correct, wrong = build(value, " Hz", [
                (n * v / length, "Omits the factor of two in the denominator.", "missing-step"),
                (v / (2 * length), "Gives the fundamental and ignores the harmonic number.", "missing-step"),
                (n * v * 2 * length, "Multiplies by the length instead of dividing.", "inverted-operation"),
                (2 * length / (n * v), "Gives a period rather than a frequency.", "unit-error")])

    elif domain == "fields":
        if depth == 0:
            q1, q2 = rng.choice([2, 3, 5, 8]), rng.choice([3, 4, 6, 10])
            r = rng.choice([0.1, 0.2, 0.5])
            value = 8.99e9 * q1 * 1e-6 * q2 * 1e-6 / r ** 2
            stem = (f"Two point charges of {q1} μC and {q2} μC sit {r:g} m apart in vacuum. Taking "
                    f"$k = 8.99 \\times 10^9$ N·m²/C², what is the force between them, to 2 "
                    f"decimal places?")
            spec = {"kind": "compute", "vars": {"q1": q1, "q2": q2, "r": r},
                    "expr": "8.99e9*q1*1e-6*q2*1e-6/r**2", "digits": 2}
            explain = (f"$F = kq_1q_2/r^2 = (8.99\\times10^9)({q1}\\times10^{{-6}})"
                       f"({q2}\\times10^{{-6}}) \\div {r:g}^2 = {fmt(value)}$ N. The microcoulombs "
                       f"must be converted before the division.")
            latex = rf"F = \frac{{kq_1q_2}}{{r^2}} = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (8.99e9 * q1 * 1e-6 * q2 * 1e-6 / r, "Does not square the separation.", "missing-step"),
                (8.99e9 * q1 * q2 / r ** 2, "Leaves the charges in microcoulombs.", "unit-error"),
                (8.99e9 * (q1 + q2) * 1e-6 / r ** 2, "Adds the charges instead of multiplying.", "wrong-operation"),
                (8.99e9 * q1 * 1e-6 * q2 * 1e-6 * r ** 2, "Multiplies by the square of the separation.", "inverted-operation")])
        elif depth == 1:
            q, field = rng.choice([2, 4, 5, 10]), rng.choice([2000, 5000, 8000])
            value = q * 1e-6 * field
            stem = (f"What force acts on a charge of {q} μC placed in a uniform electric field of "
                    f"{field} N/C?")
            spec = {"kind": "compute", "vars": {"q": q, "e": field},
                    "expr": "q*1e-6*e", "digits": 4}
            explain = (f"$F = qE = ({q}\\times10^{{-6}})({field}) = {fmt(value, 4)}$ N. The field "
                       f"is force per unit charge, so multiplying by the charge returns a force.")
            latex = rf"F = qE = ({q}\times10^{{-6}})({field}) = {fmt(value, 4)}"
            correct, wrong = build(value, " N", [
                (q * field, "Leaves the charge in microcoulombs.", "unit-error"),
                (field / (q * 1e-6), "Divides the field by the charge.", "inverted-operation"),
                (q * 1e-6 / field, "Inverts the relationship.", "inverted-operation"),
                (q * 1e-6 + field, "Adds the two quantities.", "wrong-operation")], digits=4)
        elif depth == 2:
            b, i = rng.choice([0.2, 0.5, 0.8]), rng.choice([3, 5, 8])
            length, theta = rng.choice([0.4, 0.5, 1.2]), rng.choice([30, 45, 60, 90])
            value = b * i * length * math.sin(math.radians(theta))
            stem = (f"A straight conductor of length {length:g} m carries {i} A and lies at "
                    f"{theta}° to a uniform magnetic field of {b:g} T. What force acts on it, to "
                    f"2 decimal places?")
            spec = {"kind": "compute", "vars": {"b": b, "i": i, "l": length, "th": theta},
                    "expr": "b*i*l*sin(radians(th))", "digits": 2}
            explain = (f"$F = BIL\\sin\\theta = ({b:g})({i})({length:g})\\sin{theta}° = "
                       f"{fmt(value)}$ N. The force is greatest at 90° and vanishes when the "
                       f"conductor lies along the field.")
            latex = rf"F = BIL\sin\theta = ({b:g})({i})({length:g})\sin{theta}° = {fmt(value)}"
            correct, wrong = build(value, " N", [
                (b * i * length * math.cos(math.radians(theta)), "Uses the cosine of the angle.", "wrong-rule"),
                (b * i * length, "Ignores the angle entirely.", "missing-step"),
                (b * i / length * math.sin(math.radians(theta)), "Divides by the length.", "inverted-operation"),
                (b * length * math.sin(math.radians(theta)), "Leaves the current out.", "missing-step")])
        else:
            turns, dphi = rng.choice([50, 100, 200, 400]), rng.choice([0.02, 0.05, 0.1])
            dt = rng.choice([0.1, 0.2, 0.5])
            value = turns * dphi / dt
            stem = (f"The flux through a {turns}-turn coil changes by {dphi:g} Wb in {dt:g} s. "
                    f"What is the magnitude of the emf induced in it?")
            spec = {"kind": "compute", "vars": {"n": turns, "p": dphi, "t": dt},
                    "expr": "n*p/t", "digits": 2}
            explain = (f"Faraday's law gives $|\\varepsilon| = N\\Delta\\Phi/\\Delta t = "
                       f"{turns}({dphi:g}) \\div {dt:g} = {fmt(value)}$ V. The minus sign in the "
                       f"law is Lenz's law, which fixes direction rather than size.")
            latex = rf"|\varepsilon| = N\frac{{\Delta\Phi}}{{\Delta t}} = {turns}\frac{{{dphi:g}}}{{{dt:g}}} = {fmt(value)}"
            correct, wrong = build(value, " V", [
                (dphi / dt, "Leaves out the number of turns.", "missing-step"),
                (turns * dphi * dt, "Multiplies by the time instead of dividing.", "inverted-operation"),
                (turns * dt / dphi, "Inverts the rate of change.", "inverted-operation"),
                (turns * dphi, "Stops before dividing by the time.", "missing-step")])

    elif domain == "ac":
        if depth == 0:
            peak = rng.choice([4, 10, 14, 20])
            value = peak / math.sqrt(2)
            stem = (f"An alternating current has a peak value of {peak} A. What is its RMS value, "
                    f"to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"p": peak}, "expr": "p/sqrt(2)", "digits": 2}
            explain = (f"$I_{{rms}} = I_{{max}}/\\sqrt2 = {peak} \\div 1.414 = {fmt(value)}$ A. "
                       f"The RMS value is the direct current that would heat a resistor equally.")
            latex = rf"I_{{rms}} = \frac{{I_{{max}}}}{{\sqrt2}} = \frac{{{peak}}}{{\sqrt2}} = {fmt(value)}"
            correct, wrong = build(value, " A", [
                (peak * math.sqrt(2), "Multiplies by root two instead of dividing.", "inverted-operation"),
                (peak / 2, "Halves the peak instead of dividing by root two.", "wrong-rule"),
                (peak, "Treats the peak value as the RMS value.", "no-change"),
                (peak * 2, "Doubles the peak value.", "scale-error")])
        elif depth == 1:
            henry, f = rng.choice([50, 100, 200, 400]), rng.choice([50, 60, 400])
            value = 2 * math.pi * f * henry / 1000
            stem = (f"What is the reactance of a {henry} mH inductor at {f} Hz, to 2 decimal "
                    f"places?")
            spec = {"kind": "compute", "vars": {"l": henry, "f": f},
                    "expr": "2*pi*f*l/1000", "digits": 2}
            explain = (f"$X_L = 2\\pi f L = 2\\pi({f})({henry / 1000:g}) = {fmt(value)}$ Ω, with "
                       f"the inductance first converted to henries. Reactance rises with "
                       f"frequency, so an inductor blocks fast changes.")
            latex = rf"X_L = 2\pi f L = 2\pi({f})({henry / 1000:g}) = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (2 * math.pi * f * henry, "Leaves the inductance in millihenries.", "unit-error"),
                (1 / (2 * math.pi * f * henry / 1000), "Uses the capacitive formula instead.", "wrong-rule"),
                (f * henry / 1000, "Omits the factor of two pi.", "missing-step"),
                (2 * math.pi * henry / 1000 / f, "Divides by the frequency.", "inverted-operation")])
        elif depth == 2:
            cap, f = rng.choice([1, 2, 4, 10]), rng.choice([50, 60, 400])
            value = 1 / (2 * math.pi * f * cap * 1e-6)
            stem = (f"What is the reactance of {_a(cap)} {cap} μF capacitor at {f} Hz, to 2 "
                    f"decimal places?")
            spec = {"kind": "compute", "vars": {"c": cap, "f": f},
                    "expr": "1/(2*pi*f*c*1e-6)", "digits": 2}
            explain = (f"$X_C = 1/(2\\pi f C) = 1 \\div (2\\pi({f})({cap}\\times10^{{-6}})) = "
                       f"{fmt(value)}$ Ω. Reactance falls as frequency rises, which is the "
                       f"opposite of an inductor.")
            latex = rf"X_C = \frac{{1}}{{2\pi f C}} = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (2 * math.pi * f * cap * 1e-6, "Inverts the formula.", "inverted-operation"),
                (1 / (2 * math.pi * f * cap), "Leaves the capacitance in microfarads.", "unit-error"),
                (1 / (f * cap * 1e-6), "Omits the factor of two pi.", "missing-step"),
                (1 / (2 * math.pi * cap * 1e-6 / f), "Divides by the frequency instead of multiplying.", "inverted-operation")])
        else:
            r = rng.choice([30, 40, 60])
            xl, xc = rng.choice([80, 120, 160]), rng.choice([20, 40, 100])
            value = math.sqrt(r ** 2 + (xl - xc) ** 2)
            stem = (f"A series RLC circuit has R = {r} Ω, $X_L$ = {xl} Ω and $X_C$ = {xc} Ω. What "
                    f"is its impedance, to 2 decimal places?")
            spec = {"kind": "compute", "vars": {"r": r, "xl": xl, "xc": xc},
                    "expr": "sqrt(r**2+(xl-xc)**2)", "digits": 2}
            explain = (f"$Z = \\sqrt{{R^2 + (X_L - X_C)^2}} = \\sqrt{{{r}^2 + ({xl} - {xc})^2}} = "
                       f"{fmt(value)}$ Ω. The two reactances oppose each other, so they subtract "
                       f"before being combined with the resistance.")
            latex = rf"Z = \sqrt{{R^2 + (X_L-X_C)^2}} = \sqrt{{{r}^2 + ({xl}-{xc})^2}} = {fmt(value)}"
            correct, wrong = build(value, " Ω", [
                (r + xl - xc, "Adds the terms arithmetically instead of in quadrature.", "wrong-rule"),
                (math.sqrt(r ** 2 + (xl + xc) ** 2), "Adds the reactances instead of subtracting.", "sign-error"),
                (r ** 2 + (xl - xc) ** 2, "Forgets the square root.", "missing-step"),
                (math.sqrt(r ** 2 + xl ** 2 + xc ** 2), "Squares each reactance separately.", "wrong-rule")])

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
    # Adiabatic is deliberately absent: it is defined by no heat crossing the
    # boundary rather than by a quantity staying constant, so it has no honest
    # answer to this question and would make the pool dishonest if forced in.
    "constant_in_process": {
        "answers": {
            "an isothermal process": "the temperature",
            "an isochoric process": "the volume",
            "an isobaric process": "the pressure",
        },
        "pool": ["the temperature", "the volume", "the pressure",
                 "the internal energy", "the entropy"],
        "why": "A different process holds that quantity fixed.",
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
