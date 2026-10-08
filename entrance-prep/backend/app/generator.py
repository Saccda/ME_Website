"""Original bounded template families. No textbook text is loaded at runtime."""
import random
from itertools import permutations
from .catalog import DOMAINS, LEVELS
from .mathgen import template as math_template

def article(word):
    """"a" or "an" for the instrument names used below, which all begin with a
    plain consonant or vowel sound. Without this the templates produced "a
    ammeter" and "a anemometer"."""
    return "an" if word[:1].lower() in "aeiou" else "a"

def options(correct, wrong, rng, count):
    candidates = [(str(correct), "Correct reasoning", "correct")]
    seen = {str(correct)}
    for value, rationale, error in wrong:
        if str(value) not in seen:
            seen.add(str(value))
            candidates.append((str(value), rationale, error))
        if len(candidates) == count:
            break
    if len(candidates) != count:
        raise ValueError("Template lacks enough distinct distractors")
    rng.shuffle(candidates)
    return [{"id": chr(65+i), "text": t, "rationale": r, "error": e} for i, (t,r,e) in enumerate(candidates)], chr(65+next(i for i,c in enumerate(candidates) if c[0]==str(correct)))

def ordering_solutions(spec):
    result = []
    for order in permutations(spec["items"]):
        pos = {x:i for i,x in enumerate(order)}
        good = True
        for rule in spec["rules"]:
            if rule[0] == "before": good &= pos[rule[1]] < pos[rule[2]]
            elif rule[0] == "adjacent": good &= abs(pos[rule[1]]-pos[rule[2]]) == 1
            elif rule[0] == "at": good &= pos[rule[1]] == rule[2]
            elif rule[0] == "not_at": good &= pos[rule[1]] != rule[2]
            elif rule[0] == "if_before": good &= not (pos[rule[1]] < pos[rule[2]]) or pos[rule[3]] < pos[rule[4]]
            else: raise ValueError("Unknown puzzle rule")
        if good: result.append(order)
    return result

def generate(domain, level, count=4, seed=None, presentation="text", skill=None):
    rng = random.Random(seed)
    d = next(x for x in DOMAINS if x["id"] == domain)
    depth = LEVELS.index(level)
    expected_skill = d["skills"][min(depth, len(d["skills"])-1)]
    if skill and skill not in d["skills"]: raise ValueError("Skill does not belong to domain")
    if skill and skill != expected_skill:
        raise ValueError("This template skill is tied to its difficulty. Choose its matching level.")
    spec = None
    math = None
    if d.get("subject") == "math":
        stem, answer, explain, wrong, spec, math = math_template(domain, depth, rng)
    elif domain == "patterns":
        start, step = rng.randint(13, 37), rng.randint(4, 9)
        seq = [start]
        for i in range(5):
            if depth == 0: value = seq[-1]+step
            elif depth == 1: value = seq[-1]+step+i*2
            elif depth == 2: value = seq[-1]+(step if i%2==0 else -2)
            else: value = 2*seq[-1]-step
            seq.append(value)
        answer = seq.pop()
        rule = [f"Add {step} at every step.", f"The differences start at {step} and increase by 2 each time.", f"Alternate adding {step} and subtracting 2.", f"Double the previous term, then subtract {step}."][depth]
        stem = "A counter follows a fixed rule: " + ", ".join(map(str,seq)) + ". Which number comes next?"
        explain = rule + f" Applying the same rule to {seq[-1]} gives {answer}. Check the rule against every earlier step."
        wrong = [(answer+step,"Adds an extra step instead of stopping at the next term.","extra-step"),(answer-2,"Subtracts 2 without checking the current position in the rule.","wrong-rule"),(answer+1,"Introduces a change of 1 that the sequence does not support.","unsupported-step"),(seq[-1],"Repeats the last term rather than applying the rule.","no-change"),(answer-1,"Stops one unit short of the required value.","arithmetic-slip")]
        spec = {"kind":"sequence", "terms": seq, "start":start, "step":step, "family":depth}
        math = [r"a_{n+1}=a_n+"+str(step),r"a_{n+1}=a_n+"+str(step)+r"+2(n-1)",r"+"+str(step)+r",\;-2,\;+"+str(step)+r",\;-2",r"a_{n+1}=2a_n-"+str(step)][depth]
    elif domain == "symbols":
        if depth == 0:
            step = rng.randint(2,4)
            start = rng.randint(0,4)
            vals = [chr(65+start+i*step) for i in range(5)]
            answer=vals[-1]; vals=vals[:-1]
            stem = f"Using A=1 through Z=26, complete the letter pattern: {', '.join(vals)}, ?"
            explain = f"Move forward {step} alphabet positions each time. The next letter is {answer}."
            spec = {"kind":"letters","terms":vals,"step":step}
            wrong=[(chr(65+(ord(answer)-65+j)%26),f"Moves {step+j} positions instead of {step}.","alphabet-step") for j in [-2,-1,1,2,3]]
        elif depth == 1:
            cycle=rng.sample(["triangle","circle","square","diamond","star"],3)
            n=rng.randint(5,8)
            vals=[cycle[i%3] for i in range(n)]
            answer=cycle[n%3]
            stem=f"The three-shape cycle repeats: {', '.join(vals)}. What comes next?"
            explain=f"The repeating block is {' → '.join(cycle)}. The next position in that block is {answer}."
            wrong=[(v,"This shape is not at the next position in the repeating block.","cycle-position") for v in ["triangle","circle","square","diamond","star"] if v!=answer]
            spec={"kind":"cycle","terms":vals,"cycle":cycle}
        elif depth == 2:
            start=rng.randint(0,3); step=rng.randint(2,4); number=rng.randint(11,24); increment=rng.randint(3,7)
            vals=[chr(65+start+i*step)+str(number+i*increment) for i in range(4)]
            answer=chr(65+start+4*step)+str(number+4*increment)
            stem=f"Letters use A=1 through Z=26. Each letter and number follows its own fixed-step rule: {', '.join(vals)}, ? Which pair is next?"
            explain=f"Letters advance {step} positions and numbers increase by {increment}. Apply both rules to obtain {answer}."
            wrong=[(chr(65+start+4*step+a)+str(number+4*increment+b),f"Changes {'the letter step' if a else 'the number increment'} while the other component may appear plausible.","paired-rule-error") for a,b in [(0,-increment),(0,increment),(1,0),(-1,0),(1,increment)]]
            spec={"kind":"paired","terms":vals,"start":start,"step":step,"number":number,"increment":increment}
        else:
            start=rng.randint(0,3); jumps=[rng.randint(2,3),rng.randint(4,5)]; positions=[start]
            for i in range(5):positions.append(positions[-1]+jumps[i%2])
            answer=chr(65+positions[-1]);vals=[chr(65+x) for x in positions[:-1]]
            stem=f"Using A=1 through Z=26, complete the alternating-step pattern: {', '.join(vals)}, ?"
            explain=f"The jumps alternate +{jumps[0]}, +{jumps[1]}. The next jump is +{jumps[0]}, giving {answer}. Check both rules across the whole sequence."
            wrong=[(chr(65+(positions[-1]+j)%26),"Applies the wrong jump or introduces an unsupported alphabet position.","alternating-step-error") for j in [-2,-1,1,2,3]]
            spec={"kind":"alternating_letters","terms":vals,"start":start,"jumps":jumps}
    elif domain == "relationships":
        item = rng.choice([("thermometer","temperature","ruler","length"),("balance","mass","clock","time"),("speedometer","speed","pressure gauge","pressure"),("caliper","length","voltmeter","voltage"),("ammeter","current","anemometer","air speed"),("sound meter","sound level","force gauge","force"),("humidity meter","humidity","thermometer","temperature"),("pressure gauge","pressure","balance","mass")])
        a,b,c,answer=item
        if depth == 0:
            stem=f"Which category do {article(a)} {a} and {article(c)} {c} both belong to?"
            answer="A measuring instrument"
            wrong=[("A source of power","These tools measure rather than supply energy.","category-confusion"),("A raw material","These are finished tools, not materials.","category-confusion"),("A communication network","The common function is measurement.","function-confusion"),("A transport route","Neither object is a route.","category-confusion")]
            explain="Both tools obtain measurements. Classify by their shared function, rather than by material or appearance."
        elif depth == 1:
            stem=f"Complete the functional analogy: {a} is to {b} as {c} is to _____."
            wrong=[(v,f"{article(c).capitalize()} {c} does not measure this quantity.","wrong-quantity") for v in ["voltage","brightness","volume","angle","density","temperature","mass"] if v!=answer]
            explain=f"The relationship is instrument → quantity measured. {article(c).capitalize()} {c} measures {answer}. Keep the direction of the relationship unchanged."
        elif depth == 2:
            stem=f"{article(c).capitalize()} {c} is defined here as a tool that reports {answer}. Which property is essential to meeting that definition?"
            answer=f"It produces a measurement of {answer}."
            wrong=[("It has a digital display.","Analog tools can meet the definition.","incidental-feature"),("It is powered by a battery.","Power source is not part of the definition.","incidental-feature"),("It is made of metal.","Material is not required by the definition.","incidental-feature"),("It is used indoors.","Location is not part of the definition.","incidental-feature")]
            explain="An essential property must follow from the given definition. Display, power, material, and location can vary."
        else:
            stem=f"{article(a).capitalize()} {a} measures {b}. A technician uses that reading to decide whether a process meets a specified limit. Which chain preserves these relationships?"
            answer="Instrument → measurement → comparison with limit → decision"
            wrong=[("Decision → instrument → limit → measurement","The decision requires the measurement and comparison first.","reversed-chain"),("Instrument → decision → measurement → comparison","A decision cannot precede the evidence it uses.","premature-conclusion"),("Limit → instrument → decision → measurement","The reading must be obtained before the decision.","reversed-chain"),("Measurement → limit → instrument → decision","The instrument produces the measurement.","reversed-chain")]
            explain="Preserve cause and purpose at each link: obtain a reading, compare it with the specified criterion, then decide."
    elif domain == "codes":
        p,q,r=rng.sample(["vemi","daku","sori","nelo","batu","fena"],3)
        if depth == 0:
            stem=f"In an invented language, {p}{q} means 'small wheel', {p}{r} means 'small motor', and {q}{r} means 'wheel motor'. What does {q} mean?"
            answer="wheel"; explain=f"{p} is shared by the phrases with 'small'. {q} is shared by the two phrases with 'wheel', so {q} means wheel."
        elif depth == 1:
            stem=f"Compounds preserve word order. {p}{q} means 'solar pump'; {p}{r} means 'solar station'; {q}{r} means 'pump station'. What does {p}{q}{r} mean?"
            answer="solar pump station"; explain=f"Shared components show {p}=solar, {q}=pump, {r}=station. Decode all three in the stated order."
        elif depth == 2:
            stem=f"Compounds preserve word order. {p}{q} means 'solar pump'; {q}{r} means 'pump station'; {p}{r} means 'solar station'. Which compound means 'station solar pump'?"
            answer=r+p+q; explain=f"Map {p}=solar, {q}=pump, {r}=station, then reverse the mapping: station solar pump becomes {answer}."
        else:
            stem=f"Each component has one meaning and compounds preserve order: {p}{q}='solar pump', {q}{r}='pump station', {p}{r}='solar station'. A label {r}{q}{p} appears on a model. Which interpretation satisfies all three clues?"
            answer="station pump solar"; explain=f"The shared-component mapping is unique: {p}=solar, {q}=pump, {r}=station. Decode {r}{q}{p} in order, using all three clues."
        if depth==0:
            pool=["motor","small","station","solar","pump"]
            pairs=[[[p,q],["small","wheel"]],[[p,r],["small","motor"]],[[q,r],["wheel","motor"]]]
            target=[q]
        else:
            meanings=["solar","pump","station"]
            pool=[''.join(x) if depth==2 else ' '.join(x) for x in permutations([p,q,r] if depth==2 else meanings)]
            pairs=[[[p,q],["solar","pump"]],[[q,r],["pump","station"]],[[p,r],["solar","station"]]]
            target=["station","solar","pump"] if depth==2 else [p,q,r] if depth==1 else [r,q,p]
        wrong=[(v,"The shared components fix each meaning. This option assigns a different meaning or changes the required order.","code-mapping") for v in pool if v!=answer]
        spec={"kind":"language","pairs":pairs,"target":target,"encode":depth==2}
    elif domain == "verbal":
        equipment=rng.choice(['cutter','lathe','drill press','parts scanner','test rig'])
        trained_name,other_name=rng.sample(['Dara','Lina','Sokha','Mony','Sophea','Vanna','Rithy'],2)
        component=rng.choice(['belt','filter','bearing','seal','coupling'])
        if depth == 0:
            stem=f"For this exercise, preventive maintenance of a {equipment} means servicing equipment before a fault occurs. Which action matches the definition?"
            answer=f"Replacing a {component} on its scheduled service date before failure."
            explain="The service occurs before a fault. Responding after failure is corrective maintenance."
            wrong=[("Replacing a belt after it snaps.","This responds to an existing fault.","definition-mismatch"),("Repairing a motor after it stops.","The failure has already occurred.","definition-mismatch"),("Recording last year's repair costs.","Recording information is not servicing equipment.","irrelevant-action"),("Moving a broken pump to storage.","No preventive servicing is performed.","definition-mismatch")]
        else:
            stem=f"In a fictional workshop, every person operating the {equipment} must complete safety training. "
            # Each depth carries its own distractors. A shared list put permits,
            # inspectors and a second name into stems that never introduce them,
            # leaving options that referred to nothing in the question.
            if depth==1:
                stem+="Dara operates the cutter. What must be true?"
                answer="Dara completed safety training."
                explain="Apply the necessary condition: operating the cutter implies completed training. Training alone does not imply permission to operate it."
                wrong=[("Every trained person operates the cutter.","A necessary condition is not a sufficient condition.","converse-error"),("Completing safety training is enough to operate the cutter.","Training is required by the rule, not made sufficient by it.","sufficiency-confusion"),("Dara did not complete safety training.","This contradicts the rule applied to a stated operator.","contradiction"),("Only Dara completed safety training.","The stem says nothing about anyone else's training.","unsupported-inference"),("Nobody who completed training operates the cutter.","This contradicts the case stated in the question.","contradiction")]
            elif depth==2:
                stem+="Some trained people are inspectors. Lina has not completed training. What must be true?"
                answer="Lina does not operate the cutter."
                explain="By contrapositive, someone without the required training cannot be a cutter operator. The fact about some inspectors gives no conclusion about Lina."
                wrong=[("Every trained person operates the cutter.","A necessary condition is not a sufficient condition.","converse-error"),("Lina must be an inspector.","A statement about some people does not identify Lina.","some-to-all"),("No trained person can be an inspector.","The premises explicitly allow trained inspectors.","contradiction"),("Lina completed safety training.","This contradicts what the question states about Lina.","contradiction"),("Every inspector operates the cutter.","Nothing connects being an inspector to operating the machine.","unsupported-inference")]
            else:
                stem+="Every cutter operator also has a permit; some trained permit holders are inspectors. Lina lacks training but has a permit. What must be true?"
                answer="Lina does not operate the cutter."
                explain="Training and a permit are both necessary. A permit alone is insufficient. Lina lacks training, so she cannot be an operator; her inspector status is unknown."
                wrong=[("Every trained person operates the cutter.","A necessary condition is not a sufficient condition.","converse-error"),("Lina must be an inspector.","A statement about some people does not identify Lina.","some-to-all"),("A permit alone guarantees cutter operation.","This ignores the training requirement.","ignored-condition"),("No trained person can be an inspector.","The premises explicitly allow trained inspectors.","contradiction"),("Lina completed safety training.","This contradicts what the question states about Lina.","contradiction")]
            # Substitute the machine everywhere, including "cutter operator";
            # matching only "the cutter" left two different machines in one stem
            # and made the worked explanation untrue.
            stem=stem.replace('Dara',trained_name).replace('Lina',other_name).replace('cutter',equipment)
            answer=answer.replace('Dara',trained_name).replace('Lina',other_name).replace('cutter',equipment)
            explain=explain.replace('Dara',trained_name).replace('Lina',other_name).replace('cutter',equipment)
            wrong=[(v.replace('Dara',trained_name).replace('Lina',other_name).replace('cutter',equipment),r.replace('Dara',trained_name).replace('Lina',other_name).replace('cutter',equipment),e) for v,r,e in wrong]
    elif domain == "deduction":
        items=["A","B","C","D","E"]
        order=rng.sample(items,5)
        if depth==0:
            rules=[["before",order[i],order[i+1]] for i in range(4)]
        elif depth==1:
            rules=[["at",order[0],0],["adjacent",order[1],order[2]],["before",order[1],order[2]],["before",order[2],order[3]],["before",order[3],order[4]]]
        elif depth==2:
            rules=[["at",order[0],0],["at",order[4],4],["before",order[1],order[2]],["if_before",order[0],order[4],order[2],order[3]]]
        else:
            rules=[["at",order[0],0],["not_at",order[4],3],["adjacent",order[1],order[2]],["before",order[1],order[2]],["before",order[2],order[3]],["if_before",order[0],order[3],order[3],order[4]]]
        descriptions=[]
        for rule in rules:
            kind=rule[0]
            if kind=="before": descriptions.append(f"{rule[1]} is before {rule[2]}")
            elif kind=="adjacent": descriptions.append(f"{rule[1]} and {rule[2]} are adjacent")
            elif kind=="at": descriptions.append(f"{rule[1]} is in position {rule[2]+1}")
            elif kind=="not_at": descriptions.append(f"{rule[1]} is not in position {rule[2]+1}")
            else: descriptions.append(f"if {rule[1]} is before {rule[2]}, then {rule[3]} is before {rule[4]}")
        pos=rng.randint(1,3)
        spec={"kind":"ordering","items":items,"rules":rules,"position":pos}
        sols=ordering_solutions(spec)
        values={x[pos] for x in sols}
        if len(values)!=1: raise ValueError("Ambiguous template")
        answer=next(iter(values))
        stem="Five test stations A, B, C, D, and E occupy positions 1–5 from left to right. Each appears exactly once. Rules: " + "; ".join(descriptions) + f". Which station must occupy position {pos+1}?"
        explain="Apply every rule together. The only valid order is " + " → ".join(sols[0]) + f". Therefore position {pos+1} contains {answer}."
        wrong=[(v,"Placing this station here violates at least one stated ordering constraint.","ignored-constraint") for v in items if v!=answer]
    else:
        place=rng.choice(["a fictional Phnom Penh workshop","a hypothetical provincial training center","a fictional student project team","a fictional Battambang repair center","a fictional Siem Reap fabrication team","a hypothetical Kampong Cham workshop","a fictional laboratory exercise","a hypothetical machine service team"])
        if depth==0:
            stem=f"At {place}, repeat measurements vary widely. The supervisor says, 'We should calibrate the gauge because reliable measurements are needed before comparing parts.' Which statement is the conclusion?"
            answer="The gauge should be calibrated."
            explain="The conclusion is the proposed action. The need for reliable measurements is the supporting reason."
            wrong=[("Reliable measurements are needed.","This is a reason supporting the action.","premise-conclusion"),("The supervisor spoke.","This reports the speaker rather than the argument's conclusion.","irrelevant-detail"),("All parts are identical.","This claim is not stated or supported.","unsupported-inference"),("Calibration is always free.","No cost claim is given.","unsupported-inference")]
        elif depth==1:
            stem=f"At {place}, a team proposes a new gauge to reduce measurement errors. Its argument is that the new gauge has finer graduations. Which assumption links this feature to the proposed benefit?"
            answer="Reading resolution contributes to the team's current measurement errors."
            explain="Finer graduations help only if resolution is relevant to the existing errors. The argument needs this link between feature and benefit."
            wrong=[("Every new gauge is cheaper.","Price does not connect resolution to errors.","irrelevant-evidence"),("The old gauge has a different color.","Color is not the reasoning link.","irrelevant-evidence"),("The team never makes mistakes.","This would remove the problem rather than support the proposal.","contradiction"),("All errors are caused by the weather.","This undermines the relevance of finer graduations.","causal-confounding")]
        elif depth==2:
            stem=f"At {place}, output increased after a scheduling app was introduced. A manager concludes that the app caused the increase. Which additional fact most weakens that causal conclusion?"
            answer="The workshop also added a second production shift that week."
            explain="The second shift offers an alternative explanation for increased output. Timing alone does not establish which change caused the improvement."
            wrong=[("The app has a blue icon.","Appearance does not explain output.","irrelevant-evidence"),("Output was measured weekly.","Frequency alone provides no alternative cause.","irrelevant-evidence"),("The manager likes the app.","Preference is not evidence about the cause.","opinion-as-evidence"),("The app was installed before output increased.","This repeats the timing and does not weaken the conclusion.","correlation-causation")]
        else:
            stem=f"At {place}, volunteers who attended optional tool training made fewer errors than those who did not. The organizer concludes that requiring everyone to attend will produce the same reduction. Which issue most directly challenges that inference?"
            answer="Volunteers may already have been more careful or experienced before training."
            explain="Self-selection can confound the comparison. The groups may differ before training, so the observed difference cannot be attributed solely to training or generalized automatically to everyone."
            wrong=[("The training room had windows.","This does not explain the group difference.","irrelevant-evidence"),("The organizer wants fewer errors.","The goal does not establish causation.","opinion-as-evidence"),("Some tools are heavier than others.","No difference in tool use between groups is established.","unsupported-inference"),("The volunteers attended training.","This restates the observation without examining the inference.","premise-conclusion")]
    opts, correct = options(answer, wrong, rng, count)
    return {"stem":stem,"options":opts,"correct":correct,"explanation":explain,"math":math,"presentation":presentation,"asset":None,"asset_alt":"","diagram":({"kind":"stations","labels":["1","2","3","4","5"]} if domain=="deduction" else {"kind":"cycle","labels":spec["terms"]} if spec and spec["kind"] in ("cycle","letters","paired","alternating_letters") else {"kind":"flow","labels":["Observe","Find rule","Test","Conclude"]}) if presentation=="diagram" else None,"validator":spec,"skill":expected_skill}
