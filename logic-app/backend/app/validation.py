import ast, base64, math, re
from .generator import ordering_solutions

# A bounded arithmetic evaluator. Mathematics and physics answers are computable,
# so the server recomputes them instead of trusting the author's key. Only the
# nodes listed here are reachable, so a question cannot smuggle in code.
FUNCTIONS = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
             "asin": math.asin, "acos": math.acos, "atan": math.atan,
             "atan2": math.atan2, "radians": math.radians, "degrees": math.degrees,
             "log": math.log, "log10": math.log10, "exp": math.exp,
             "abs": abs, "round": round, "min": min, "max": max}

def safe_number(expr, variables):
    if not isinstance(expr, str) or len(expr) > 240: raise ValueError("expression too long")
    def walk(node):
        if isinstance(node, ast.Expression): return walk(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)): raise ValueError()
            return node.value
        if isinstance(node, ast.Name):
            if node.id == "pi": return math.pi
            if node.id not in variables: raise ValueError()
            return variables[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = walk(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp):
            left, right = walk(node.left), walk(node.right)
            op = node.op
            if isinstance(op, ast.Add): return left + right
            if isinstance(op, ast.Sub): return left - right
            if isinstance(op, ast.Mult): return left * right
            if isinstance(op, ast.Div): return left / right
            if isinstance(op, ast.Mod): return left % right
            if isinstance(op, ast.Pow):
                # Bound the work, not the legitimate range: 2**12 is ordinary,
                # while 1e6**32 would be an attempt to hang the server.
                if abs(right) > 32 or abs(left) > 1e6: raise ValueError()
                if left == 0 and right < 0: raise ValueError()
                if left < 0 and right != int(right): raise ValueError()
                if left and abs(right) * math.log10(abs(left) or 1) > 12: raise ValueError()
                return left ** right
            raise ValueError()
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.keywords: raise ValueError()
            fn = FUNCTIONS.get(node.func.id)
            if fn is None or len(node.args) > 2: raise ValueError()
            return fn(*[walk(a) for a in node.args])
        raise ValueError()
    value = walk(ast.parse(expr, mode="eval"))
    if not isinstance(value, (int, float)) or value != value or abs(value) > 1e12: raise ValueError()
    return float(value)

def leading_number(text):
    found = re.search(r"-?\d+(?:\.\d+)?(?:\s*(?:×|x|\*)\s*10\s*\^?\s*(-?\d+))?",
                      str(text).replace(",", "").replace("−", "-"))
    if not found: return None
    value = float(found.group().split("×")[0].split("x")[0].split("*")[0].strip())
    return value * (10 ** int(found.group(1))) if found.group(1) else value

def validate(content):
    errors=[]
    opts=content.get("options",[])
    ids=[x.get("id") for x in opts]
    texts=[x.get("text","").strip().casefold() for x in opts]
    if len(opts) not in (4,5): errors.append("MCQ requires exactly 4 or 5 options.")
    if ids != list("ABCDE"[:len(opts)]): errors.append("Option IDs must be consecutive A–E.")
    if len(set(texts))!=len(texts) or not all(texts): errors.append("Options must be distinct and non-empty.")
    if content.get("correct") not in ids: errors.append("Select exactly one valid answer.")
    if not content.get("stem","").strip() or not content.get("explanation","").strip(): errors.append("Stem and worked explanation are required.")
    if any(not x.get("rationale","").strip() or not x.get("error") for x in opts): errors.append("Every option needs rationale and an error tag.")
    if content.get("presentation") not in ("text","image","diagram"): errors.append("Unknown presentation type.")
    asset=content.get("asset")
    if content.get("presentation")=="image":
        if not asset or not content.get("asset_alt","").strip(): errors.append("Image questions need an image and descriptive alt text.")
    if asset:
        match=re.fullmatch(r"data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)",asset)
        if not match or len(asset)>2800000: errors.append("Image must be PNG/JPEG/WebP under 2 MB.")
        else:
            try:
                raw=base64.b64decode(match[2],validate=True)
                valid=(match[1]=="png" and raw.startswith(b'\x89PNG\r\n\x1a\n')) or (match[1]=="jpeg" and raw.startswith(b'\xff\xd8')) or (match[1]=="webp" and raw[:4]==b'RIFF' and raw[8:12]==b'WEBP')
                if not valid: errors.append("Image signature does not match the declared format.")
            except Exception: errors.append("Invalid image encoding.")
    if content.get("presentation")=="diagram":
        diagram=content.get("diagram") or {}
        if diagram.get("kind") not in ("stations","cycle","flow") or not isinstance(diagram.get("labels"),list) or not 1<=len(diagram["labels"])<=12: errors.append("Provide 1–12 labels for a supported diagram.")
    spec=content.get("validator")
    expected=None
    proof=None
    if spec:
        try:
            if len(str(spec))>12000: raise ValueError()
            if spec["kind"]=="sequence":
                if not isinstance(spec["terms"],list) or not 2<=len(spec["terms"])<=30 or not all(isinstance(x,(int,float)) and abs(x)<10**12 for x in spec["terms"]): raise ValueError()
                if not all(isinstance(spec.get(k),(int,float)) and abs(spec[k])<10**9 for k in ("start","step")): raise ValueError()
                seq=[spec["start"]]
                for i in range(len(spec["terms"])):
                    f,s=spec["family"],spec["step"]
                    if f not in (0,1,2,3): raise ValueError()
                    seq.append(seq[-1]+s if f==0 else seq[-1]+s+i*2 if f==1 else seq[-1]+(s if i%2==0 else -2) if f==2 else seq[-1]*2-s)
                if seq[:-1]!=spec["terms"]: errors.append("Sequence terms conflict with validator.")
                expected=str(seq[-1]); proof="Recomputed every term from the declared rule."
            elif spec["kind"]=="letters":
                vals=spec["terms"]
                if not 2<=len(vals)<=20 or any(not isinstance(x,str) or not re.fullmatch('[A-Z]',x) for x in vals) or not isinstance(spec['step'],int) or not 1<=spec['step']<=25: raise ValueError()
                if any(ord(b)-ord(a)!=spec["step"] for a,b in zip(vals,vals[1:])): errors.append("Letter pattern conflicts with rule.")
                expected=chr(ord(vals[-1])+spec["step"]); proof="Checked every alphabet step."
            elif spec["kind"]=="cycle":
                c=spec["cycle"]
                if not isinstance(c,list) or not 2<=len(c)<=8 or not 2<=len(spec["terms"])<=30: raise ValueError()
                if spec["terms"]!=[c[i%len(c)] for i in range(len(spec["terms"]))]: errors.append("Cycle terms conflict with rule.")
                expected=c[len(spec["terms"])%len(c)]; proof="Checked every cycle position."
            elif spec['kind']=='alphabet_blocks':
                blocks=spec['blocks'];missing=spec['missing'];width=spec['width'];step=spec['step'];start=spec['start']
                if not 2<=len(blocks)<=8 or not 0<=missing<len(blocks) or not 1<=width<=5 or step not in (-1,1) or not re.fullmatch('[A-Z]',start): raise ValueError()
                sequence=[chr(ord(start)+step*i) for i in range(width*len(blocks))]
                if any(not re.fullmatch('[A-Z]',letter) for letter in sequence): raise ValueError()
                computed=[''.join(sequence[i*width:(i+1)*width]) for i in range(len(blocks))]
                if any(block!=computed[i] for i,block in enumerate(blocks) if i!=missing) or blocks[missing] is not None: errors.append('Alphabet blocks conflict with the continuous rule.')
                expected=computed[missing];proof='Reconstructed the continuous alphabet run and verified every given block.'
            elif spec['kind']=='paired':
                vals=spec['terms']
                if not 2<=len(vals)<=10: raise ValueError()
                seq=[chr(65+spec['start']+i*spec['step'])+str(spec['number']+i*spec['increment']) for i in range(len(vals)+1)]
                if seq[:-1]!=vals: errors.append('Paired sequence conflicts with component rules.')
                expected=seq[-1]; proof='Recomputed both letter and number components.'
            elif spec['kind']=='alternating_letters':
                vals=spec['terms'];jumps=spec['jumps']
                if len(jumps)!=2 or not 2<=len(vals)<=10: raise ValueError()
                positions=[spec['start']]
                for i in range(len(vals)): positions.append(positions[-1]+jumps[i%2])
                seq=[chr(65+x) for x in positions]
                if seq[:-1]!=vals: errors.append('Alternating letter terms conflict with rules.')
                expected=seq[-1];proof='Checked both alternating alphabet jumps.'
            elif spec['kind']=='language':
                mapping={}
                if len(spec['pairs'])>12 or len(spec['target'])>8: raise ValueError()
                for encoded, meanings in spec['pairs']:
                    if len(encoded)!=len(meanings): raise ValueError()
                    for part,meaning in zip(encoded,meanings):
                        if part in mapping and mapping[part]!=meaning: raise ValueError()
                        mapping[part]=meaning
                if len(set(mapping.values()))!=len(mapping): raise ValueError()
                expected=''.join({v:k for k,v in mapping.items()}[x] for x in spec['target']) if spec['encode'] else ' '.join(mapping[x] for x in spec['target'])
                proof='Unified every component clue and applied the one-to-one mapping in order.'
            elif spec["kind"]=="ordering":
                if not isinstance(spec['items'],list) or not 2<=len(spec["items"])<=7 or len(set(spec["items"]))!=len(spec["items"]) or len(spec['rules'])>25 or not isinstance(spec['position'],int) or not 0<=spec['position']<len(spec['items']): raise ValueError()
                sols=ordering_solutions(spec)
                values={x[spec["position"]] for x in sols}
                if len(values)!=1: errors.append("Puzzle has no unique answer to the target position.")
                else: expected=next(iter(values))
                proof=f"Enumerated all arrangements: {len(sols)} satisfy all constraints."
            elif spec["kind"]=="compute":
                variables=spec.get("vars") or {}
                if not isinstance(variables,dict) or len(variables)>12: raise ValueError()
                if any(isinstance(v,bool) or not isinstance(v,(int,float)) or abs(v)>1e9 for v in variables.values()): raise ValueError()
                value=safe_number(spec["expr"],variables)
                digits=spec.get("digits")
                if digits is not None:
                    if not isinstance(digits,int) or not 0<=digits<=6: raise ValueError()
                    value=round(value,digits)
                tolerance=spec.get("tolerance",1e-6)
                if not isinstance(tolerance,(int,float)) or not 0<=tolerance<=1e6: raise ValueError()
                margin=max(float(tolerance),abs(value)*1e-9)
                keyed=leading_number(next((x["text"] for x in opts if x["id"]==content.get("correct")),""))
                if keyed is None or abs(keyed-value)>margin:
                    errors.append("Answer key conflicts with the recomputed value.")
                # Two options holding the same value would make the question unanswerable.
                for other in opts:
                    if other["id"]==content.get("correct"): continue
                    number=leading_number(other.get("text",""))
                    if number is not None and abs(number-value)<=margin:
                        errors.append("A distractor equals the correct value.")
                        break
                proof=f"Recomputed {spec['expr']} from the stated values; result {value:g}."
            else: errors.append("Unknown validator.")
            correct=next((x["text"] for x in opts if x["id"]==content.get("correct")),None)
            if expected is not None and str(correct)!=expected: errors.append("Answer key conflicts with deterministic result.")
        except (KeyError, TypeError, ValueError, IndexError, OverflowError): errors.append("Malformed validator specification.")
    return {"passed":not errors,"errors":errors,"method":"deterministic" if spec else "editorial","proof":proof,"requires_human":True,"note":"Deterministic checks verify the structured rule, not the natural-language stem. Review wording, ambiguity, relevance, and distractors before approval."}
