#!/usr/bin/env python3
"""FixErrorGuide static site generator — phase 1.
Data verified against manufacturer documentation and cross-checked references (2026-11-26).
Each code page: meaning, causes ranked, safe checks, repair cost, when to call a pro."""
import json, os, html

OUT = os.path.join(os.path.dirname(__file__), "public")
os.makedirs(OUT, exist_ok=True)

CODES = [
 # ---------------- LG WASHER ----------------
 dict(brand="LG", appliance="Washer", code="OE", slug="lg-washer-oe-error",
   meaning="Drain error — the washer cannot drain water out within the allowed time.",
   causes=["Clogged drain pump filter (the most common cause — coins, lint and small items collect there)",
           "Kinked, blocked or frozen drain hose",
           "Drain pump impeller jammed or pump motor failed",
           "Drain hose installed too high (over about 96 in / 244 cm total rise)"],
   checks=["Unplug the washer. Open the small panel at the bottom front and place a shallow tray and towel underneath.",
           "Unscrew the drain filter slowly, let the water run out through the small emergency hose first if fitted, then remove and clean the filter.",
           "Check the drain hose along its full length for kinks and blockages, and make sure it is not pushed too far down the standpipe.",
           "Plug back in and run a rinse-and-spin cycle. If OE returns with a clean filter and clear hose, the pump itself is the likely fault."],
   cost="Filter/hose fix: $0 DIY. Drain pump replacement: roughly $120–$250 with a technician, or $30–$60 for the part alone.",
   pro="Call a pro if the pump makes no sound at all during drain, if water leaks from underneath, or if the code returns after cleaning the filter."),
 dict(brand="LG", appliance="Washer", code="UE", slug="lg-washer-ue-error",
   meaning="Unbalanced load — the washer cannot distribute the laundry evenly enough to spin safely.",
   causes=["Laundry clumped on one side (single heavy item such as a blanket or bath mat)",
           "Load too small or too large",
           "Washer not level on the floor",
           "Worn suspension rods or shock absorbers (on older machines, when UE happens on almost every load)"],
   checks=["Pause the cycle, open the door and redistribute the laundry evenly around the drum. Add one or two similar items if washing a single heavy piece.",
           "Remove some items if the drum is packed full.",
           "Check the machine does not rock when you push its top corners; adjust the leveling feet until it is solid.",
           "Run the spin again. Occasional UE is normal; UE on every load points to worn suspension parts."],
   cost="$0 if it is just the load. Suspension rods/shocks: roughly $100–$220 fitted.",
   pro="Call a pro if UE appears on nearly every load even with balanced, medium loads and a level machine."),
 dict(brand="LG", appliance="Washer", code="IE", slug="lg-washer-ie-error",
   meaning="Inlet error — not enough water is entering the washer within the allowed time.",
   causes=["Water taps not fully open",
           "Clogged mesh filters in the inlet hoses",
           "Kinked inlet hoses or low household water pressure",
           "Faulty water inlet valve or frozen pipes in winter"],
   checks=["Make sure both hot and cold taps are fully open.",
           "Turn off the taps, unscrew the inlet hoses from the back of the washer and clean the small mesh filters inside the valve inlets.",
           "Straighten any kinks in the hoses and check water pressure at a nearby tap.",
           "Reconnect, and run a wash cycle. If IE returns with good pressure and clean filters, the inlet valve is the likely fault."],
   cost="$0 for taps/filters. Inlet valve replacement: roughly $130–$250 fitted.",
   pro="Call a pro if the valve buzzes but no water enters, or if there is any sign of leaking at the valve."),
 dict(brand="LG", appliance="Washer", code="dE", slug="lg-washer-de-error",
   meaning="Door error — the washer thinks the door is not closed or the door lock has not engaged. Variants dE1 and dE2 point to the door lock switch/sensor.",
   causes=["Door not fully closed or laundry caught in the seal",
           "Damaged or misaligned door latch/strike",
           "Failed door lock assembly (common on front loaders)",
           "Wiring fault between the lock and the control board (dE2)"],
   checks=["Open the door, check nothing is trapped in the rubber seal, and close it firmly until it clicks.",
           "Inspect the door strike (the plastic/metal catch on the door) for cracks or looseness.",
           "Unplug the machine for 5 minutes to reset the control, then try again.",
           "If the door visibly closes and latches but dE stays, the lock assembly has usually failed."],
   cost="$0 if it was laundry in the seal. Door lock replacement: roughly $120–$230 fitted; the part is typically $25–$60.",
   pro="Call a pro if the door will not unlock with laundry inside, or if you see scorch marks around the lock connector."),
 dict(brand="LG", appliance="Washer", code="LE", slug="lg-washer-le-error",
   meaning="Motor error — the motor is locked or overloaded and the drum cannot turn properly.",
   causes=["Overloaded drum or a very heavy single item",
           "Foreign object jammed between the drum and tub",
           "Failed rotor position (hall) sensor on direct-drive models",
           "Loose wiring to the motor or a faulty stator"],
   checks=["Unplug the washer for 10 minutes to let the motor cool and the control reset.",
           "Remove some laundry if the drum was overloaded, then try a smaller load.",
           "With the machine empty and unplugged, turn the drum by hand — it should rotate smoothly. Grinding or a hard stop suggests a jammed object.",
           "If LE returns on a light, empty load, the cause is electrical (sensor/stator), not the laundry."],
   cost="$0 for an overload reset. Hall sensor: roughly $120–$200 fitted. Stator/motor work: $250+.",
   pro="Call a pro if LE appears with an empty drum — sensor and motor diagnosis needs a multimeter."),
 dict(brand="LG", appliance="Washer", code="FE", slug="lg-washer-fe-error",
   meaning="Overflow error — the washer has filled with too much water.",
   causes=["Water inlet valve stuck open (water keeps entering even when it should stop)",
           "Faulty water-level (pressure) sensor or a blocked/disconnected pressure hose",
           "Excessive suds confusing the level sensing"],
   checks=["Turn off the water taps immediately if the drum is overfilling.",
           "Unplug the machine. If water continues to flow in with the power off, the inlet valve is mechanically stuck and must be replaced — keep the taps off.",
           "Run a drain-only cycle to empty the drum.",
           "If the level looked normal, check for oversudsing (too much or non-HE detergent) and run a rinse."],
   cost="Inlet valve: roughly $130–$250 fitted. Pressure sensor: roughly $110–$200 fitted.",
   pro="Call a pro promptly — an overflow fault can flood. If water enters with the machine unplugged, keep taps closed until the valve is replaced."),
 dict(brand="LG", appliance="Washer", code="PE", slug="lg-washer-pe-error",
   meaning="Pressure sensor error — the water-level sensor is not reporting correctly to the control board.",
   causes=["Failed water-level (pressure) sensor",
           "Pressure hose disconnected, kinked or blocked with residue",
           "Loose or corroded sensor wiring connector"],
   checks=["Unplug the machine for 5 minutes and restart — a one-off PE can be a glitch.",
           "If PE returns before or during filling, stop the cycle.",
           "The sensor and its thin air hose sit at the top of the tub; checking them means removing the top panel — only do this if you are comfortable, with the machine unplugged.",
           "Blow gently through the pressure hose (disconnected from the sensor) to confirm it is clear."],
   cost="Pressure sensor replacement: roughly $110–$200 fitted; the part is usually $15–$40.",
   pro="Call a pro if you are not comfortable removing panels — sensor testing needs a multimeter and the part must match your model."),
 dict(brand="LG", appliance="Washer", code="tE", slug="lg-washer-te-error",
   meaning="Heating sensor error — the thermistor that measures water temperature is faulty or out of range.",
   causes=["Failed thermistor (temperature sensor)",
           "Loose or damaged thermistor wiring",
           "Heating element fault confusing the temperature reading (less common)"],
   checks=["Unplug the washer for 10 minutes and restart the cycle — note whether tE appears right away or during heating.",
           "Try a cold-water wash: if the machine completes cold cycles but fails on hot ones, the heating circuit is involved.",
           "Beyond this, diagnosis means testing the thermistor resistance at the heater assembly — technician territory for most owners."],
   cost="Thermistor replacement: roughly $110–$190 fitted. Heating element: roughly $150–$280 fitted.",
   pro="Call a pro for tE in most cases — it is an electrical diagnosis, and there is no safe DIY part swap without testing first."),
 dict(brand="LG", appliance="Washer", code="CL", slug="lg-washer-cl-error",
   meaning="Not an error — CL means Child Lock (Control Lock) is switched on, so the buttons are disabled.",
   causes=["Child Lock was activated intentionally or by accident"],
   checks=["On most LG models, press and hold the Child Lock button (often labelled, or the two buttons marked with a small lock icon) for 3 seconds to switch it off.",
           "On many models it is the 'Temp.' + 'Rinse' buttons, or a dedicated lock button — check the panel markings around the buttons for a lock symbol.",
           "The display returns to normal once CL clears. No repair is needed."],
   cost="$0 — CL is a feature, not a fault.",
   pro="No pro needed. If buttons stay unresponsive after turning CL off, unplug for 5 minutes; if still dead, the control panel may be faulty."),
 # ---------------- SAMSUNG WASHER ----------------
 dict(brand="Samsung", appliance="Washer", code="4C", slug="samsung-washer-4c-error",
   meaning="Water supply error (4C, older models 4E) — the washer is not filling with water properly.",
   causes=["Water taps closed or not fully open",
           "Clogged mesh filters in the water inlets",
           "Kinked inlet hose or low water pressure",
           "Frozen hoses in winter, or a failed inlet valve"],
   checks=["Confirm both supply taps are fully open and water pressure is normal elsewhere in the home.",
           "Close the taps, disconnect the inlet hoses at the washer and clean the mesh filters.",
           "Check the hoses for kinks and make sure the drain hose is not inserted too far into the standpipe (which can siphon water out as fast as it fills).",
           "Restart the cycle. Persistent 4C with good pressure means the inlet valve or its wiring needs testing."],
   cost="$0 for taps/filters. Inlet valve: roughly $130–$250 fitted.",
   pro="Call a pro if 4C returns with verified pressure and clean filters."),
 dict(brand="Samsung", appliance="Washer", code="5C", slug="samsung-washer-5c-error",
   meaning="Drain error (5C, shown as 5E/SE or nd on some models) — water is not draining from the drum.",
   causes=["Clogged debris (pump) filter on front loaders",
           "Blocked or kinked drain hose",
           "Drain pump jammed by a coin or button, or pump failed"],
   checks=["Unplug the machine. On front loaders, open the bottom-front flap, drain via the emergency hose into a tray, then unscrew and clean the debris filter.",
           "Check the drain hose for kinks and blockages and confirm the standpipe is not blocked.",
           "Run a spin-only cycle and listen: a humming pump with no draining means a jam or a failed pump."],
   cost="$0 for a filter clean. Drain pump: roughly $120–$250 fitted.",
   pro="Call a pro if the filter and hose are clear but the machine still will not drain."),
 dict(brand="Samsung", appliance="Washer", code="UE", slug="samsung-washer-ue-error",
   meaning="Unbalanced load error (UE/UB) — the washer cannot balance the load for spinning.",
   causes=["Single heavy item or laundry bunched to one side",
           "Too few items (one towel can trigger it)",
           "Machine not level, or worn dampers on older machines"],
   checks=["Redistribute the load evenly; add an item or two if washing one heavy piece.",
           "Make sure the machine sits level and does not rock.",
           "If UE happens on most loads, the suspension is likely worn."],
   cost="$0 for load/level fixes. Dampers: roughly $100–$220 fitted.",
   pro="Call a pro if UE is constant on normal, balanced loads."),
 dict(brand="Samsung", appliance="Washer", code="dC", slug="samsung-washer-dc-error",
   meaning="Door error (dC, shown as dE on some models) — the door is open or the door lock is not engaging.",
   causes=["Door not fully shut or laundry in the seal",
           "Damaged door latch or lock switch",
           "On AddWash models, the extra door not closed properly"],
   checks=["Open and firmly re-close the door; check the seal for trapped clothing.",
           "Inspect the latch for damage and clean around the lock.",
           "Power off for 5 minutes and retry. A door that latches but still shows dC usually needs a new lock."],
   cost="$0 if obstruction. Door lock: roughly $120–$230 fitted.",
   pro="Call a pro if the door is stuck locked with laundry inside."),
 dict(brand="Samsung", appliance="Washer", code="LC", slug="samsung-washer-lc-error",
   meaning="Leak error (LC, shown as LE on some models) — the leak sensor has detected water in the base of the machine.",
   causes=["Leaking hose connection or internal hose",
           "Too much detergent causing overflow of suds",
           "Damaged door seal or drain pump housing"],
   checks=["Unplug the machine and turn off the water supply.",
           "Check behind and under the machine for water and inspect hose connections.",
           "Let the base dry fully (this can take many hours) — the code may clear once the sensor is dry, but only run the machine while watching it, to find whether it leaks again.",
           "If it leaks again, stop using it until the source is found."],
   cost="Hose/seal fixes: roughly $100–$250 fitted depending on the part.",
   pro="Call a pro if you cannot see where the water comes from — internal leaks need panel removal."),
 dict(brand="Samsung", appliance="Washer", code="SUD", slug="samsung-washer-sud-error",
   meaning="Excess suds (SUD/5d) — the washer has detected too much foam and pauses to let it break down.",
   causes=["Too much detergent, or non-HE detergent in a high-efficiency machine",
           "Detergent build-up in the drum over time"],
   checks=["Wait — the machine usually clears SUD by itself once the suds settle.",
           "Run an empty rinse or a tub-clean cycle.",
           "Use HE detergent and reduce the dose — most loads need far less than the cap suggests."],
   cost="$0.",
   pro="No pro needed unless SUD appears even with tiny amounts of HE detergent, which can point to a sensor issue."),
]

CSS = """
:root{--navy:#0a2540;--navy2:#0e3a66;--org:#ff6b1a;--org2:#ff8a3d;--ink:#182638;--mut:#5a6b82;--bg:#f3f6fb;--card:#fff;--line:#dde6f2;--lg:#a50034;--ss:#1428a0;--ok:#0b6e4f}
*{box-sizing:border-box}body{margin:0;font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.65}
h1,h2,h3,.disp{font-family:'Archivo','Inter',sans-serif}
a{color:var(--org)}
header.site{position:sticky;top:0;z-index:50;background:linear-gradient(90deg,var(--navy),var(--navy2));color:#fff;box-shadow:0 2px 14px rgba(10,37,64,.25)}
.hwrap{max-width:1060px;margin:0 auto;padding:10px 18px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff}
.logo .wm{font-family:'Archivo';font-weight:900;font-size:22px;letter-spacing:.2px;line-height:1}
.logo .wm b{color:var(--org2);font-weight:900}
.logo small{display:block;font-family:'Inter';font-weight:500;font-size:11px;color:#a9c3de;letter-spacing:.4px}
nav.main{margin-left:auto;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
nav.main a{color:#dbe7f5;text-decoration:none;font-weight:600;font-size:14px}
nav.main a:hover{color:#fff}
.social{display:flex;gap:8px}
.social a{width:34px;height:34px;border-radius:9px;background:#fff;display:inline-flex;align-items:center;justify-content:center}
.social a:hover{background:#fff;opacity:.85}
.social svg{width:19px;height:19px}
.hero{background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 60%,#155e8a 100%);color:#fff;padding:52px 18px 46px;text-align:center}
.hero h1{font-size:42px;font-weight:900;line-height:1.12;margin:0 0 12px}
.hero h1 .hl{color:var(--org2)}
.hero p{max-width:640px;margin:0 auto 22px;color:#cfe0f2;font-size:17px}
.searchbox{max-width:560px;margin:0 auto;background:#fff;border-radius:14px;padding:6px;display:flex;gap:6px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.searchbox input{flex:1;border:0;outline:0;font-size:16px;padding:10px 12px;font-family:'Inter'}
.searchbox button{background:var(--org);color:#fff;border:0;border-radius:10px;padding:10px 20px;font-weight:700;font-family:'Archivo';cursor:pointer}
.stats{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:26px}
.stat{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:10px 18px;text-align:center}
.stat b{display:block;font-family:'Archivo';font-size:22px;font-weight:900;color:#fff}
.stat span{font-size:12px;color:#a9c3de}
main{max-width:1060px;margin:0 auto;padding:26px 18px 60px}
main.narrow{max-width:820px}
h1.ptitle{font-size:32px;line-height:1.25;margin:8px 0 12px;font-weight:800}
h2{font-size:22px;margin:30px 0 10px;font-weight:800}
.kicker{font-family:'Archivo';font-weight:800;font-size:12px;letter-spacing:1.6px;text-transform:uppercase;color:var(--org)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:14px 0;box-shadow:0 2px 10px rgba(10,37,64,.05)}
.meaning{font-size:18px;margin:0}
ul,ol{margin:8px 0 8px 20px;padding:0}li{margin:6px 0}
ol.steps{list-style:none;margin:14px 0;padding:0;counter-reset:st}
ol.steps li{counter-increment:st;position:relative;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px 14px 58px;margin:10px 0}
ol.steps li::before{content:counter(st);position:absolute;left:14px;top:12px;width:30px;height:30px;border-radius:50%;background:var(--org);color:#fff;font-family:'Archivo';font-weight:900;display:flex;align-items:center;justify-content:center;font-size:15px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin:14px 0}
.grid a{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 12px;text-decoration:none;color:var(--ink);text-align:center;transition:.15s;box-shadow:0 2px 8px rgba(10,37,64,.04)}
.grid a:hover{transform:translateY(-3px);border-color:var(--org);box-shadow:0 8px 20px rgba(10,37,64,.12)}
.grid a .cd{display:block;font-family:'Archivo';font-weight:900;font-size:24px;color:var(--navy)}
.grid a .br{font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--mut)}
.grid a.hide{display:none}
.brandgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin:16px 0}
.brandcard{border-radius:16px;padding:22px;color:#fff;text-decoration:none;display:block;transition:.15s}
.brandcard:hover{transform:translateY(-3px)}
.brandcard h3{margin:0 0 4px;font-size:24px;font-weight:900}
.brandcard p{margin:0;color:rgba(255,255,255,.85);font-size:14px}
.b-lg{background:linear-gradient(135deg,#a50034,#d61f55)}
.b-ss{background:linear-gradient(135deg,#1428a0,#2f6fd0)}
.codehead{display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.codebadge{font-family:'Archivo';font-weight:900;font-size:52px;line-height:1;color:#fff;background:linear-gradient(135deg,var(--navy),var(--navy2));border-radius:16px;padding:16px 24px;box-shadow:0 8px 22px rgba(10,37,64,.25)}
.codebadge small{display:block;font-size:12px;font-family:'Inter';font-weight:700;letter-spacing:1.5px;color:var(--org2)}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}
.pill{font-size:12.5px;font-weight:700;border-radius:999px;padding:5px 12px;background:#eef3fa;color:var(--navy);border:1px solid var(--line)}
.pill.org{background:#fff1e8;color:#b34a00;border-color:#ffd9c2}
.pill.grn{background:#e7f6f0;color:var(--ok);border-color:#bfe8d8}
.crumb{font-size:13px;color:var(--mut)}.crumb a{color:var(--navy2);text-decoration:none;font-weight:600}
.note{background:#fff8e6;border:1px solid #ecd27a;border-radius:12px;padding:14px 18px;font-size:14px}
.verified{display:flex;gap:10px;align-items:center;background:#e7f6f0;border:1px solid #bfe8d8;border-radius:12px;padding:12px 16px;font-size:14px;color:#084c38;margin:16px 0}
.cost{font-weight:600;font-size:17px}
.newsletter{background:linear-gradient(135deg,var(--navy),var(--navy2));color:#fff;border-radius:16px;padding:26px;margin:30px 0;text-align:center}
.newsletter h3{margin:0 0 6px;font-size:22px;font-weight:900}
.newsletter p{color:#cfe0f2;margin:0 0 16px}
.newsletter form{display:flex;gap:6px;max-width:480px;margin:0 auto;background:#fff;padding:6px;border-radius:12px}
.newsletter input{flex:1;border:0;outline:0;padding:10px 12px;font-size:15px;font-family:'Inter'}
.newsletter button{background:var(--org);color:#fff;border:0;border-radius:9px;padding:10px 18px;font-weight:700;font-family:'Archivo';cursor:pointer}
footer.site{background:var(--navy);color:#cfe0f2;margin-top:20px}
.fwrap{max-width:1060px;margin:0 auto;padding:34px 18px 22px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px}
footer.site h4{color:#fff;font-family:'Archivo';margin:0 0 10px;font-size:15px}
footer.site a{color:#cfe0f2;text-decoration:none;display:block;margin:5px 0;font-size:14px}
footer.site a:hover{color:#fff}
.fbot{border-top:1px solid rgba(255,255,255,.14);padding:14px 18px;text-align:center;font-size:12.5px;color:#8fa9c4;max-width:1060px;margin:0 auto}
footer.site .social a{background:#fff}
@media(max-width:640px){.hero h1{font-size:31px}.codebadge{font-size:40px}h1.ptitle{font-size:26px}}
"""

LOGO_SVG = """<svg width="42" height="42" viewBox="0 0 48 48" aria-hidden="true"><rect x="2" y="2" width="44" height="44" rx="11" fill="#ff6b1a"/><path d="M30.6 12.2a7.4 7.4 0 0 0-6.9 9.6L12 33.5a4.14 4.14 0 1 0 5.9 5.9l11.6-11.7a7.4 7.4 0 0 0 9.7-7l-4.9 4.9-3.3-1-1-3.3 4.6-4.9z" fill="#fff"/></svg>"""

SOC = {
 "youtube": ("https://www.youtube.com/@FixErrorGuide", "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"),
 "pinterest": ("https://www.pinterest.com/fixerrorguide/", "M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.162-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.345-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.401.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.354-.629-2.758-1.379l-.749 2.848c-.269 1.045-1.004 2.352-1.498 3.146 1.123.345 2.306.535 3.55.535 6.607 0 11.985-5.365 11.985-11.987C23.97 5.39 18.592.026 11.985.026L12.017 0z"),
 "facebook": ("https://www.facebook.com/fixerrorguide", "M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"),
 "x": ("https://x.com/fixerrorguide", "M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"),
}
SOC_COLORS = {"youtube": "#FF0000", "pinterest": "#E60023", "facebook": "#1877F2", "x": "#000000"}
def social_html():
    return "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}"><svg viewBox="0 0 24 24"><path fill="{SOC_COLORS[n]}" d="{p}"/></svg></a>' for n,(u,p) in SOC.items())

FAVICON = "data:image/svg+xml," + ("%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect x='2' y='2' width='44' height='44' rx='11' fill='%23ff6b1a'/%3E%3Cpath d='M30.6 12.2a7.4 7.4 0 0 0-6.9 9.6L12 33.5a4.14 4.14 0 1 0 5.9 5.9l11.6-11.7a7.4 7.4 0 0 0 9.7-7l-4.9 4.9-3.3-1-1-3.3 4.6-4.9z' fill='%23fff'/%3E%3C/svg%3E")

NEWSLETTER = """
<div class="newsletter"><h3>Get the free Washer Error Code Cheat Sheet</h3>
<p>Every LG and Samsung washer code on one printable page: what it means and the first safe check. Plus one decoded code and one do-it-yourself fix in your inbox, every week.</p>
<form action="https://buttondown.com/api/emails/embed-subscribe/fixerrorguide" method="post" target="_blank"><input type="email" name="email" required placeholder="Your email address"><button type="submit">Send my cheat sheet</button></form>
<p style="margin:12px 0 0;font-size:13px">Free PDF &middot; No spam &middot; Unsubscribe anytime</p>
<p style="margin:6px 0 0;font-size:13px">Rather not wait for the email? <a href="/washer-error-code-cheat-sheet.pdf">Download the cheat sheet directly</a></p></div>
"""

def page(title, body, desc, hero=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | FixErrorGuide</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="google-site-verification" content="Zue3je6DCsjs6V7oQCbEP70AU7M6sKepnncszhgXf2c">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3KF128VQSR"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3KF128VQSR');</script>
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<header class="site"><div class="hwrap">
<a class="logo" href="/index.html">{LOGO_SVG}<span><span class="wm">Fix<b>Error</b>Guide</span><small>APPLIANCE ERROR CODES, DECODED</small></span></a>
<nav class="main"><a href="/index.html">Home</a><a href="/lg-washer-error-codes.html">LG Codes</a><a href="/samsung-washer-error-codes.html">Samsung Codes</a><a href="/faq.html">FAQ</a><a href="/about.html">About</a><a href="/contact.html">Ask a Fix</a><span class="social">{social_html()}</span></nav>
</div></header>
{hero}
<main>{body}</main>
<footer class="site"><div class="fwrap">
<div><a class="logo" href="/index.html">{LOGO_SVG}<span><span class="wm">Fix<b>Error</b>Guide</span><small>APPLIANCE ERROR CODES, DECODED</small></span></a>
<p style="font-size:14px;margin:12px 0 0">Every code checked against the manufacturer's own documentation — what it means, what caused it, and what a fair repair costs.</p></div>
<div><h4>Popular codes</h4><a href="/lg-washer-oe-error.html">LG OE — drain error</a><a href="/samsung-washer-4c-error.html">Samsung 4C — water supply</a><a href="/lg-washer-ue-error.html">LG UE — unbalanced load</a><a href="/samsung-washer-5c-error.html">Samsung 5C — drain error</a></div>
<div><h4>Follow FixErrorGuide</h4><div class="social">{social_html()}</div><p style="font-size:13.5px">New codes and repair walk-throughs every week, on every channel.</p></div>
</div>
<div class="fbot">FixErrorGuide — Always unplug an appliance and turn off its water supply before any check. When in doubt, call a qualified technician.</div>
</footer>
</body></html>"""

DIFF = {"OE":"Easy DIY","UE":"Easy DIY","IE":"Easy DIY","CL":"Easy DIY","4C":"Easy DIY","5C":"Easy DIY","SUD":"Easy DIY",
        "dE":"Moderate DIY","dC":"Moderate DIY","FE":"Moderate DIY","LC":"Moderate DIY","LE":"Pro recommended","PE":"Pro recommended","tE":"Pro recommended"}

urls = ["index.html"]
# code pages
for c in CODES:
    lis = "".join(f"<li>{html.escape(x)}</li>" for x in c["causes"])
    ols = "".join(f"<li>{html.escape(x)}</li>" for x in c["checks"])
    rel = "".join(f'<a href="/{i["slug"]}.html"><span class="br">{i["brand"]} {i["appliance"]}</span><span class="cd">{i["code"]}</span></a>'
                  for i in CODES if i["brand"] == c["brand"] and i["code"] != c["code"])
    code_schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"What does {c['brand']} washer error code {c['code']} mean?",
             "acceptedAnswer": {"@type": "Answer", "text": c["meaning"]}},
            {"@type": "Question", "name": f"Can I fix {c['brand']} error code {c['code']} myself?",
             "acceptedAnswer": {"@type": "Answer", "text": f"Difficulty: {DIFF.get(c['code'], 'Moderate DIY')}. Start with the safe checks in this guide; if the code returns, a technician is recommended."}}]},
        ensure_ascii=False) + "</script>"
    body = f"""
<p class="crumb"><a href="/index.html">Home</a> › <a href="/{c['brand'].lower()}-washer-error-codes.html">{c['brand']} {c['appliance']} error codes</a> › {c['code']}</p>
<div class="codehead"><div class="codebadge"><small>{c['brand']} {c['appliance']}</small>{c['code']}</div>
<div><h1 class="ptitle" style="margin:0">{c['brand']} {c['appliance']} Error Code {c['code']}</h1>
<div class="pills"><span class="pill org">{DIFF.get(c['code'],'Moderate DIY')}</span><span class="pill grn">Checked against {c['brand']} documentation</span><span class="pill">Updated Nov 2026</span></div></div></div>
<div class="card"><p class="kicker">What it means</p><p class="meaning">{html.escape(c['meaning'])}</p></div>
<h2>Most likely causes</h2><ul>{lis}</ul>
<h2>Safe checks you can do yourself</h2><ol class="steps">{ols}</ol>
<h2>What a repair usually costs</h2><div class="card"><p class="cost">{html.escape(c['cost'])}</p></div>
<h2>When to call a professional</h2><p>{html.escape(c['pro'])}</p>
<div class="verified"><span>✔</span><span><strong>Verified source:</strong> this guide was checked against {c['brand']}'s official documentation for this code, and cross-checked with technician references, on 26 Nov 2026.</span></div>
<div class="note">Safety first: unplug the washer and close its water taps before opening any panel or filter. Codes can vary slightly between models — your user manual is the final reference for your exact machine.</div>
<h2>More {c['brand']} washer codes</h2><div class="grid">{rel}</div>
<div class="card" style="border-color:var(--org);background:#fff8f2"><p class="kicker">Still stuck?</p>
<p style="margin:4px 0 10px"><strong>Ask a Fix:</strong> tell us your brand, model and the code you are seeing — unlisted codes go to the top of our research list and the answer becomes a published guide.</p>
<a href="/contact.html" style="display:inline-block;background:var(--org);color:#fff;text-decoration:none;font-weight:700;font-family:'Archivo';padding:11px 20px;border-radius:10px">Ask about my code →</a>
<p style="margin:10px 0 0;font-size:13px;color:var(--mut)">Every answer is checked against the manufacturer's documentation before it is published.</p></div>
{code_schema}
{NEWSLETTER}
"""
    fn = c["slug"] + ".html"
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(page(f"{c['brand']} {c['appliance']} {c['code']} Error", body,
                     f"{c['brand']} washer error code {c['code']}: {c['meaning']} Causes, safe DIY checks and repair costs."))
    urls.append(fn)

# brand hubs + index
brands = {}
for c in CODES:
    brands.setdefault(c["brand"], []).append(c)
hub_links = ""
for b, items in brands.items():
    cards = "".join(f'<a href="/{i["slug"]}.html"><span class="br">{b} Washer</span><span class="cd">{i["code"]}</span></a>' for i in items)
    hub = f'<p class="crumb"><a href="/index.html">Home</a> › {b}</p><p class="kicker">{b} washing machines</p><h1 class="ptitle">{b} Washer Error Codes</h1><p>Every {b} washing machine error code we cover, with its meaning, the most likely causes, safe checks and typical repair costs — each one checked against {b}\'s own documentation.</p><div class="grid">{cards}</div>{NEWSLETTER}'
    fn = b.lower() + "-washer-error-codes.html"
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(page(f"{b} Washer Error Codes", hub, f"Complete list of {b} washing machine error codes with meanings, causes and fixes."))
    urls.append(fn)
    cls = "b-lg" if b == "LG" else "b-ss"
    hub_links += f'<a class="brandcard {cls}" href="/{fn}"><h3>{b}</h3><p>{len(items)} washer error codes decoded →</p></a>'

allcards = "".join(f'<a data-q="{i["brand"]} {i["code"]} {i["appliance"]}" href="/{i["slug"]}.html"><span class="br">{i["brand"]} {i["appliance"]}</span><span class="cd">{i["code"]}</span></a>' for i in CODES)
hero = f"""
<div class="hero"><h1>Your appliance is talking.<br><span class="hl">We decode it.</span></h1>
<p>Type the code on your display — get what it means, what most likely caused it, what you can safely fix yourself, and what a fair repair costs.</p>
<div class="searchbox"><input id="q" type="text" placeholder="Try: LG OE, Samsung 4C, UE…"><button onclick="document.getElementById('codes').scrollIntoView({{behavior:'smooth'}})">Find my code</button></div>
<div class="stats"><div class="stat"><b>{len(CODES)}+</b><span>codes decoded</span></div><div class="stat"><b>{len(brands)}</b><span>brands covered</span></div><div class="stat"><b>100%</b><span>checked vs manuals</span></div><div class="stat"><b>$0</b><span>cost to use</span></div></div></div>
<script>
document.getElementById('q').addEventListener('input',function(){{var v=this.value.toLowerCase().trim();document.querySelectorAll('#codes a').forEach(function(a){{a.classList.toggle('hide',v!==''&&a.dataset.q.toLowerCase().indexOf(v)===-1);}});}});
</script>
"""
index_body = f"""
<p class="kicker">Start with your brand</p><h2 style="margin-top:4px">Error codes by brand</h2>
<div class="brandgrid">{hub_links}</div>
<p class="kicker" id="codes">Most searched right now</p><h2 style="margin-top:4px">Popular error codes</h2>
<div class="grid">{allcards}</div>
<div class="verified"><span>✔</span><span><strong>How we work:</strong> every guide on FixErrorGuide is checked against the manufacturer's own documentation before it is published — no copied forums, no guessed meanings.</span></div>
<div class="note">We are building the most complete, carefully checked error-code database on the web — brand by brand, code by code. Dishwasher, dryer, refrigerator and oven codes are being added now.</div>
{NEWSLETTER}
"""
with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(page("Appliance Error Codes — Meanings, Causes & Fixes", index_body,
                 "Look up any appliance error code: what it means, likely causes, safe DIY checks and repair costs, by brand.", hero=hero))

ABOUT = f"""
<p class="kicker">About us</p>
<h1 class="ptitle">FixErrorGuide — repair knowledge, minus the guesswork</h1>
<p>FixErrorGuide exists for one moment: your washer, dryer or dishwasher stops, flashes a code you have never seen, and you have to decide — fix it yourself, or pay for a service call? We turn that code into a clear answer: what it means, what most likely caused it, what you can safely check yourself in the next 20 minutes, and what a fair repair should cost if you do call a professional.</p>
<h2>By the numbers</h2>
<div class="stats" style="justify-content:flex-start">
<div class="stat" style="background:#eef3fa;border-color:var(--line)"><b style="color:var(--navy)">{len(CODES)}+</b><span style="color:var(--mut)">codes decoded so far</span></div>
<div class="stat" style="background:#eef3fa;border-color:var(--line)"><b style="color:var(--navy)">2</b><span style="color:var(--mut)">brands, growing weekly</span></div>
<div class="stat" style="background:#eef3fa;border-color:var(--line)"><b style="color:var(--navy)">100%</b><span style="color:var(--mut)">checked vs manufacturer docs</span></div>
</div>
<h2>How every guide is made</h2>
<ul><li><strong>Source first:</strong> the meaning of every code is taken from the manufacturer's own documentation for that brand — never copied from forums.</li>
<li><strong>Causes ranked:</strong> the most common cause comes first, because that is what it usually is.</li>
<li><strong>Safety boundaries:</strong> each guide separates safe owner checks from jobs that need a technician, and says so plainly.</li>
<li><strong>Honest costs:</strong> typical US repair ranges, parts and labour, so a quote can be judged before anyone is paid.</li></ul>
<h2>What we cover</h2>
<p>Washing machines today; dryers, dishwashers, refrigerators and ovens are being added brand by brand, code by code. New guides are published every week.</p>
{NEWSLETTER}
"""
with open(os.path.join(OUT, "about.html"), "w") as f:
    f.write(page("About FixErrorGuide", ABOUT, "About FixErrorGuide: how our appliance error-code guides are researched, verified and written."))
urls.append("about.html")

FAQS = [
 ("My machine shows a code that is not listed here. What do I do?",
  "Codes grow with every model year, and we add new ones weekly. Note the exact code and your model number, check your user manual's troubleshooting table, and send us the code through the Ask a Fix page — unlisted codes go to the top of our research list."),
 ("Is it safe to keep running the machine with an error code showing?",
  "For balance (UE) and suds (SUD) codes, yes after fixing the load or letting suds settle. For leak (LC/LE), overflow (FE) or any burning smell, stop immediately, unplug the machine and close the water taps."),
 ("Why do repair costs vary so much between quotes?",
  "Labour rates differ by city, and some faults share one code. Every guide here gives the typical range for parts and labour, so you can tell a fair quote from an inflated one before you agree to anything."),
 ("Are your guides copied from the manufacturers' websites?",
  "No. Meanings are verified against manufacturer documentation, then rewritten as ranked causes, safe step-by-step checks and cost guidance — the parts manuals never give you."),
 ("The code cleared after unplugging. Is the machine fixed?",
  "Maybe — a reset clears one-off glitches. If the same code returns within a few cycles, treat it as a real fault and follow the guide for that code."),
 ("Do you sell parts or send technicians?",
  "Not today. FixErrorGuide is an independent information site; our guides tell you honestly when a job is DIY-safe and when to hire a local professional."),
]
faq_items = "".join(f'<div class="card"><h3 style="margin:0 0 6px;font-size:17px">{html.escape(q)}</h3><p style="margin:0">{html.escape(a)}</p></div>' for q, a in FAQS)
FAQ = f"""
<p class="kicker">Good questions</p>
<h1 class="ptitle">Frequently asked questions</h1>
{faq_items}
{NEWSLETTER}
"""
FAQ += '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]},
    ensure_ascii=False) + "</script>"
with open(os.path.join(OUT, "faq.html"), "w") as f:
    f.write(page("FAQ — Appliance Error Codes", FAQ, "Answers to the most common questions about appliance error codes, safety, repair costs and how FixErrorGuide works."))
urls.append("faq.html")

CONTACT = """
<p class="kicker">Ask a fix</p>
<h1 class="ptitle">Tell us your code — we will decode it</h1>
<p>Machine showing a code we have not covered yet, or a guide that did not solve it? Send the details below. Unlisted codes go to the top of our research list, and the answer is published as a new guide for everyone.</p>
<div class="card"><form onsubmit="event.preventDefault();var b='Brand: '+this.brand.value+'%0D%0ACode: '+this.code.value+'%0D%0AModel: '+this.model.value+'%0D%0A%0D%0A'+encodeURIComponent(this.msg.value);window.location='mailto:contact@fixerrorguide.com?subject='+encodeURIComponent('Error code question: '+this.brand.value+' '+this.code.value)+'&body='+b;">
<p><label><strong>Brand</strong></label><br><input name="brand" required style="width:100%;padding:10px;border:1px solid var(--line);border-radius:9px;font-size:15px" placeholder="e.g. LG"></p>
<p><label><strong>Error code shown</strong></label><br><input name="code" required style="width:100%;padding:10px;border:1px solid var(--line);border-radius:9px;font-size:15px" placeholder="e.g. OE"></p>
<p><label><strong>Model number (if you know it)</strong></label><br><input name="model" style="width:100%;padding:10px;border:1px solid var(--line);border-radius:9px;font-size:15px" placeholder="On a sticker inside the door"></p>
<p><label><strong>What happened?</strong></label><br><textarea name="msg" rows="4" style="width:100%;padding:10px;border:1px solid var(--line);border-radius:9px;font-size:15px" placeholder="When does the code appear? Any noise, leaks or smells?"></textarea></p>
<button type="submit" style="background:var(--org);color:#fff;border:0;border-radius:10px;padding:12px 22px;font-weight:700;font-family:'Archivo';cursor:pointer;font-size:15px">Send my question</button>
</form></div>
<div class="note">The button opens your email app with everything filled in — just press send there. We read every question; the most-asked codes become full guides.</div>
"""
with open(os.path.join(OUT, "contact.html"), "w") as f:
    f.write(page("Ask a Fix — Contact FixErrorGuide", CONTACT, "Ask FixErrorGuide about an appliance error code: send your brand, code and model and we will research it."))
urls.append("contact.html")

THANKS_BODY = """
<p class="kicker">Newsletter</p>
<h1 class="ptitle">Almost done — check your inbox</h1>
<p>We just sent a confirmation email to the address you entered. Click the link inside it and your subscription is complete. That extra click is what keeps anyone else from signing you up without your permission.</p>
<p>No email after a few minutes? Check your Promotions or Spam folder, and drag it into your main inbox so the weekly issue reaches you.</p>
<div class="card"><p style="margin:0 0 8px"><strong>While you wait, grab your cheat sheet now:</strong></p>
<p style="margin:0"><a href="/washer-error-code-cheat-sheet.pdf">Download the Washer Error Code Cheat Sheet (PDF)</a> — every LG and Samsung washer code on one printable page.</p></div>
"""
with open(os.path.join(OUT, "thanks.html"), "w") as f:
    f.write(page("Almost done — check your inbox", THANKS_BODY, "Confirm your FixErrorGuide newsletter subscription.")
            .replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1))

CONFIRMED_BODY = """
<p class="kicker">Newsletter</p>
<h1 class="ptitle">You're in — welcome to FixError Guide</h1>
<p>Your subscription is confirmed. One email a week: one error code decoded in plain English, one fix you can safely do yourself, and what a technician would charge if you can't. No spam, ever, and one click unsubscribes you.</p>
<div class="card"><p style="margin:0 0 8px"><strong>Your free cheat sheet:</strong></p>
<p style="margin:0"><a href="/washer-error-code-cheat-sheet.pdf">Download the Washer Error Code Cheat Sheet (PDF)</a> — print it and keep it near the washer.</p></div>
<p>Machine showing a code right now? Start with the <a href="/lg-washer-error-codes.html">LG codes</a> or the <a href="/samsung-washer-error-codes.html">Samsung codes</a>.</p>
"""
with open(os.path.join(OUT, "confirmed.html"), "w") as f:
    f.write(page("You're in — subscription confirmed", CONFIRMED_BODY, "Your FixErrorGuide newsletter subscription is confirmed.")
            .replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1))

SITE_BASE = "https://fixerrorguide.netlify.app"  # switch to https://fixerrorguide.com when the domain is live
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join(f"<url><loc>{SITE_BASE}/{u}</loc></url>\n" for u in urls) + "</urlset>")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE}/sitemap.xml\n")
with open(os.path.join(OUT, "logo.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect x="2" y="2" width="44" height="44" rx="11" fill="#ff6b1a"/><path d="M30.6 12.2a7.4 7.4 0 0 0-6.9 9.6L12 33.5a4.14 4.14 0 1 0 5.9 5.9l11.6-11.7a7.4 7.4 0 0 0 9.7-7l-4.9 4.9-3.3-1-1-3.3 4.6-4.9z" fill="#fff"/></svg>')

print(f"Generated {len(urls)} pages:", ", ".join(urls))
