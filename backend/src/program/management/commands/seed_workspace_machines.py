"""File the four machines newly installed in the CDIO Engineering Learning Workspace.

The write-ups come from "Detail for each machine in ME lab", supplied by the
program. Each machine follows the same shape, which is the shape the document
itself uses: what it is, why the laboratory needs it, the principle it works
on, its main parts, and the sequence of operating it.

Nothing here is invented. Where the document gives a figure -- the 300 kN
capacity, the compressive-strength formula -- it is reproduced; where it does
not, none is supplied. Model numbers, dimensions, temperature ranges and
manufacturers are deliberately absent, because the document does not give them
and a specification is exactly the sort of thing a reader will check.

A machine already in the catalogue is left alone, so this can be run again
safely. Photographs are attached in Wagtail afterwards.

    python manage.py seed_workspace_machines
"""

from django.core.management.base import BaseCommand

from program.models import Facility, FocusArea


def para(text):
    return ("paragraph", f"<p>{text}</p>")


def steps(heading, items):
    return (
        "steps",
        {
            "heading": heading,
            "steps": [{"title": t, "description": d} for t, d in items],
        },
    )


HOT_PRESS = {
    "name": "Hydraulic Hot Press",
    "areas": ["DMP"],
    "description": (
        "Applies controlled heat and pressure for a set time, used to produce "
        "and study composite materials such as boards made from natural fibres "
        "and agricultural residue."
    ),
    "detail": [
        para(
            "A hot press processes materials by applying controlled heat and "
            "pressure together for a specific amount of time. In this "
            "laboratory it is especially useful for producing and studying "
            "composite materials, such as boards made from natural fibres or "
            "agricultural residue."
        ),
        ("heading", "Where the heat comes from"),
        para(
            "Large flat plates called platens sit inside the machine. Heating "
            "elements in or around them raise their temperature and transfer "
            "heat into the material. Depending on what is being pressed, that "
            "heat softens a polymer, activates or cures a resin binder, "
            "improves bonding between layers, helps particles consolidate into "
            "a dense board, or helps the material take the shape of a mould. "
            "Producing a composite board uses several of those at once: the "
            "heat lets the binder flow or cure while the pressure brings the "
            "particles and fibres into close contact."
        ),
        ("heading", "Why it is hydraulic"),
        para(
            "The hydraulic part is how the pressing force is generated. "
            "Hydraulic fluid transmits pressure to a cylinder, and the cylinder "
            "moves the pressing platen to apply a large compressive force."
        ),
        steps(
            "Main parts",
            [
                ("Hydraulic cylinder", "Moves the pressing platen and provides the main pressing force."),
                ("Heated platens", "The flat plates that contact the mould and material, providing heat and pressure."),
                ("Hydraulic system", "Pump, fluid, reservoir, valves and cylinder together."),
                ("Temperature controller", "Sets and monitors the required temperature."),
                ("Pressure control", "Controls the force applied to the material."),
                ("Frame", "The structure that holds the machine together and withstands the forces generated during pressing."),
            ],
        ),
        steps(
            "How it works",
            [
                ("Prepare the material", "The material is prepared for the experiment — sugarcane bagasse with a binder, for instance — with the particles and fibres distributed appropriately before pressing."),
                ("Place it in the mould", "The mould determines the shape and dimensions of the finished product. For a board, loose particles go in and a flat panel comes out."),
                ("Heat", "The heated platens transfer thermal energy into the mould and the material. The temperature required depends strongly on the material and the binder."),
                ("Apply pressure", "The hydraulic system pushes the platen against the mould, compressing the material. This reduces void space, increases contact between particles, improves consolidation and bonding, and helps the material conform to the mould."),
                ("Hold", "Temperature and pressure are maintained for a set period, the dwell time, because the material needs time for the thermal and mechanical processes to take place."),
                ("Release and remove", "Pressure is released, the mould is opened and the product removed. Depending on the material it may need to cool before being handled or tested."),
            ],
        ),
        (
            "callout",
            {
                "label": "Note",
                "text": (
                    "Exact components and configuration vary between machines; "
                    "these are the systems common to laboratory hydraulic hot "
                    "presses."
                ),
            },
        ),
    ],
}

SHREDDER = {
    "name": "Shredding Machine",
    "areas": ["DMP"],
    "description": (
        "Reduces large pieces of material into smaller ones by cutting, tearing "
        "and crushing — usually the first step in preparing plastic waste, "
        "agricultural residue or fibres for further processing."
    ),
    "detail": [
        para(
            "A shredder reduces large pieces of material into smaller pieces by "
            "applying mechanical force. In this laboratory it prepares "
            "materials such as plastic waste, agricultural residue and fibres "
            "for further processing."
        ),
        ("heading", "Why material is shredded"),
        para(
            "Material has to be reduced to a size that is easier to process, "
            "mix, transport, melt or reshape, combine with other materials, or "
            "recycle into something new. Shredding is therefore usually the "
            "first step in material processing."
        ),
        steps(
            "The three mechanisms",
            [
                ("Shearing — cutting", "Two surfaces move relative to each other and cut the material. Shearing occurs when forces act in opposite directions along or near a surface, causing it to separate."),
                ("Tearing — ripping", "Rotating cutters grab the material and pull it apart, which is particularly useful for flexible or fibrous materials."),
                ("Crushing — breaking", "Compressive force large enough to deform or fracture the material. Some machines combine crushing with cutting and tearing."),
            ],
        ),
        steps(
            "What makes the machine work",
            [
                ("Motor", "Provides the mechanical energy needed to rotate the shredding mechanism."),
                ("Transmission", "Gears, chains, belts or shafts transfer and modify the motor's rotation."),
                ("Rotating shaft", "Transfers rotational motion to the cutters."),
                ("Cutters and rotors", "The rotating components that interact with the material."),
            ],
        ),
    ],
}

COMPRESSION = {
    "name": "Compression Testing Machine (300 kN)",
    "areas": ["ECM"],
    "description": (
        "Applies a controlled compressive load of up to 300 kN to a specimen "
        "and measures the force at which it fails, giving the compressive "
        "strength of materials made in the laboratory."
    ),
    "detail": [
        para(
            "A compression testing machine applies a controlled squeezing load "
            "to a specimen — a concrete cube, a composite block — and measures "
            "the force at which it fails. The 300 kN figure is the maximum load "
            "the machine can apply. Here it is used mainly to test the "
            "mechanical strength of materials produced in-house, such as "
            "composite boards."
        ),
        ("heading", "Why compression testing matters"),
        para(
            "Almost every material used in construction or product design has "
            "to withstand compressive force in service. Testing establishes the "
            "compressive strength of a material, usually in MPa; whether it "
            "meets a required design or safety standard; how consistent a batch "
            "of samples is; and how a new formulation compares with an existing "
            "one. That is what tells an engineer whether a material suits a "
            "given structural or product application."
        ),
        ("heading", "Why it is hydraulic"),
        para(
            "As with the hot press, a hydraulic pump pressurises oil which is "
            "fed to a cylinder. The cylinder drives one platen onto the "
            "specimen, applying a steadily increasing load, while a load sensor "
            "converts the pressure into a force reading on the digital "
            "controller."
        ),
        steps(
            "Main parts",
            [
                ("Loading frame", "The rigid steel frame, with columns and cross-head, that resists the reaction force generated during a test and keeps the platens aligned."),
                ("Upper and lower platens", "Flat hardened steel plates that sandwich the specimen and transmit the load evenly across its surface."),
                ("Hydraulic cylinder and pump", "Generate and apply the compressive force to the upper platen."),
                ("Digital indicator", "Displays applied load in kN, pressure and loading rate in real time."),
                ("Loading rate control valve", "Sets how quickly the load increases, since testing standards usually require a controlled rate."),
                ("Base and cabinet", "Supports the frame and houses the hydraulic reservoir, control valves and electrical components."),
            ],
        ),
        steps(
            "How a test runs",
            [
                ("Prepare the specimen", "The specimen — a cube, cylinder or composite block — is prepared according to the relevant testing standard."),
                ("Place the specimen", "It is centred between the platens so the load is applied uniformly and axially."),
                ("Zero and set up", "The digital indicator is zeroed and the loading rate set according to the applicable standard."),
                ("Apply the load", "The hydraulic system increases the compressive force at the set rate while the display tracks it."),
                ("Record the failure load", "Loading continues until the specimen cracks or fails; the maximum load reached is the failure load."),
                ("Calculate the strength", "Compressive strength is the maximum load divided by the cross-sectional area of the specimen."),
            ],
        ),
        (
            "callout",
            {
                "label": "Formula",
                "text": (
                    "Compressive strength (MPa) = maximum load (N) ÷ "
                    "cross-sectional area (mm²). The result is the stress the "
                    "material withstood before failing, compared against design "
                    "or quality-control requirements."
                ),
            },
        ),
    ],
}

FURNACE = {
    "name": "Electric Muffle Furnace",
    "areas": ["DMP"],
    "description": (
        "A box-type resistance furnace that heats samples to high temperature "
        "in an enclosed chamber, used for ashing, sintering, calcination and "
        "heat treatment."
    ),
    "detail": [
        para(
            "An electric muffle furnace, also called a box-type resistance "
            "furnace, heats materials to high temperature inside an enclosed "
            "chamber. The word muffle refers to the sample chamber being "
            "isolated from the heating elements and from combustion "
            "by-products, so the material inside is heated cleanly. The "
            "laboratory uses it for ashing, sintering, calcination and heat "
            "treatment."
        ),
        ("heading", "Why controlled high-temperature heating"),
        para(
            "Many material-testing procedures need heat that is precise, "
            "uniform and repeatable. The furnace can burn off organic material "
            "to determine ash content, dry samples at a controlled temperature, "
            "sinter or heat-treat ceramic, metal and composite samples, anneal "
            "materials to relieve internal stress, and carry out reactions that "
            "require sustained high heat. Because the chamber is enclosed and "
            "insulated, temperatures stay stable and even throughout the "
            "sample, which makes results more repeatable."
        ),
        ("heading", "Why it is electric"),
        para(
            "Heat is generated by resistance elements embedded in or around the "
            "chamber walls. Current passing through them makes them hot, and "
            "they radiate that heat into the chamber. A temperature controller "
            "regulates the power supplied, so a target temperature can be set "
            "and held."
        ),
        steps(
            "Main parts",
            [
                ("Furnace chamber", "The enclosed inner cavity, lined with refractory insulating material, where the sample sits."),
                ("Heating elements", "Resistance wires or coils in the chamber walls that generate heat when current passes through them."),
                ("Furnace door", "Insulated, and seals the chamber to retain heat."),
                ("Temperature controller", "Sets the target temperature, shows the current chamber temperature and controls the heating."),
                ("Ammeter", "Shows the current drawn by the heating elements, useful for monitoring the furnace's condition."),
                ("Power switch", "Turns the electrical supply on and off."),
                ("Outer casing", "The steel housing that encloses and insulates the chamber and protects the operator."),
            ],
        ),
        steps(
            "How it works",
            [
                ("Prepare the sample", "The material is prepared and placed in a suitable crucible or container."),
                ("Load the sample", "The door is opened, the sample placed inside, and the door closed to seal in the heat."),
                ("Set temperature and time", "The operator sets the target temperature, and on some models a ramp rate, using the digital controller."),
                ("Heating", "Current flows through the elements, which radiate heat into the chamber while the controller holds the temperature."),
                ("Hold", "Once the set temperature is reached it is maintained for the soaking time."),
                ("Cool down and remove", "The furnace is switched off or left to cool, and the sample is removed once the chamber has cooled."),
            ],
        ),
        (
            "callout",
            {
                "label": "Safety",
                "text": (
                    "Chamber temperatures reach several hundred degrees "
                    "Celsius. Heat-resistant gloves and tongs must always be "
                    "used when loading and unloading."
                ),
            },
        ),
    ],
}

MACHINES = [HOT_PRESS, SHREDDER, COMPRESSION, FURNACE]


class Command(BaseCommand):
    help = (
        "File the four CDIO workspace machines with their write-ups. Skips any "
        "machine already in the catalogue."
    )

    def handle(self, *args, **options):
        created = skipped = 0
        highest = (
            Facility.objects.order_by("-sort_order")
            .values_list("sort_order", flat=True)
            .first()
            or 0
        )

        for spec in MACHINES:
            if Facility.objects.filter(name=spec["name"]).exists():
                skipped += 1
                self.stdout.write(f"  already present: {spec['name']}")
                continue

            highest += 1
            facility = Facility.objects.create(
                name=spec["name"],
                description=spec["description"],
                detail=spec["detail"],
                availability_status="new",
                sort_order=highest,
            )
            areas = FocusArea.objects.filter(code__in=spec["areas"])
            facility.focus_areas.set(areas)
            created += 1
            self.stdout.write(
                self.style.SUCCESS(f"  created: {facility.name} → /{facility.slug}")
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"{created} machine(s) created, {skipped} skipped.")
        )
        if created:
            self.stdout.write(
                "\nEach one still needs its photograph, added in Wagtail under"
                "\nSnippets > Facilities. The write-ups are already there."
            )
