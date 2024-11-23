from flask import Flask, render_template, request
from urllib.parse import urlencode
import random

# Initialize the Flask app
app = Flask(__name__)

# Data for random generation
race_classes = {
    "Dwarf": ["Hunter", "Paladin", "Priest", "Rogue", "Warrior"],
    "Gnome": ["Mage", "Rogue", "Warlock", "Warrior"],
    "Human": ["Mage", "Paladin", "Priest", "Rogue", "Warlock", "Warrior"],
    "Night Elf": ["Druid", "Hunter", "Priest", "Rogue", "Warrior"],
    "Orc": ["Hunter", "Rogue", "Shaman", "Warlock", "Warrior"],
    "Tauren": ["Druid", "Hunter", "Shaman", "Warrior"],
    "Troll": ["Hunter", "Mage", "Priest", "Rogue", "Shaman", "Warrior"],
    "Undead": ["Mage", "Priest", "Rogue", "Warlock", "Warrior"]
}

race_avatars = {
    "Dwarf": "static/images/Races/dwarf.png",
    "Gnome": "static/images/Races/gnome.png",
    "Human": "static/images/Races/human.png",
    "Night Elf": "static/images/Races/night_elf.png",
    "Orc": "static/images/Races/orc.png",
    "Tauren": "static/images/Races/tauren.png",
    "Troll": "static/images/Races/troll.png",
    "Undead": "static/images/Races/undead.png"
}

class_avatars = {
    "Warrior": "static/images/Classes/warrior.png",
    "Mage": "static/images/Classes/mage.png",
    "Rogue": "static/images/Classes/rogue.png",
    "Hunter": "static/images/Classes/hunter.png",
    "Warlock": "static/images/Classes/warlock.png",
    "Priest": "static/images/Classes/priest.png",
    "Druid": "static/images/Classes/druid.png",
    "Paladin": "static/images/Classes/paladin.png",
    "Shaman": "static/images/Classes/shaman.png"
}

profession_avatars = {
    "Alchemy": "static/images/Professions/alchemy.png",
    "Blacksmithing": "static/images/Professions/blacksmithing.png",
    "Enchanting": "static/images/Professions/enchanting.png",
    "Engineering": "static/images/Professions/engineering.png",
    "Herbalism": "static/images/Professions/herbalism.png",
    "Leatherworking": "static/images/Professions/leatherworking.png",
    "Mining": "static/images/Professions/mining.png",
    "Skinning": "static/images/Professions/skinning.png",
    "Tailoring": "static/images/Professions/tailoring.png"
}



class_challenges = {
    "Warrior": [
        {"name": "Shield Bearer", "description": "You must use a shield at all times and cannot equip two-handed weapons."},
        {"name": "No Armor", "description": "Wear no armor above white (common) quality."},
        {"name": "Tank Forever", "description": "You must stay in Defensive Stance at all times."},
        {"name": "No Shouts", "description": "Battle Shout and Demoralizing Shout are off-limits."},
        {"name": "Berserker Mode", "description": "You must stay in Berserker Stance at all times."},
        {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
        {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
        {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
        {"name": "Unkillable", "description": "Prioritize stamina gear above all other stats."},
        {"name": "1v1 me Bro", "description": "Fight only one enemy at a time; avoid cleave or AoE abilities."},
        {"name": "Warrior Monk", "description": "Avoid all rage-spending abilities. Use auto-attacks only."},
{"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    ],

"Hunter": [
    {"name": "Untamer", "description": "You cannot use any pet."},
    {"name": "Melee Hunter", "description": "Use only melee weapons and abilities in combat."},
    {"name": "Trapless Hunter", "description": "Avoid using traps in any encounter."},
    {"name": "Ammo Limit", "description": "Carry only one stack of arrows or bullets at a time."},
    {"name": "No Aspect of the Cheetah/Pact", "description": "Movement speed boosts are forbidden."},
    {"name": "No Feigner", "description": "You cannot use feign death."},
    {"name": "Nuzlocke", "description": "Use the same pet until it dies. If it dies, release it and tame a new one."},
    {"name": "Defender Pet", "description": "Your pet cannot attack enemies but may tank for you."},
    {"name": "One Weapon Only", "description": "Use only one weapon type (e.g., bow or axe) throughout."},
    {"name": "Ranged Purist", "description": "Fight exclusively with ranged attacks—no melee allowed."},
    {"name": "No Pet Food", "description": "Do not feed your pet; maintain loyalty through fights only."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
],

"Mage": [
    {"name": "Arcane Purist", "description": "Use only Arcane spells for damage and utility."},
    {"name": "Pyromaniac", "description": "Use only Fire spells for damage."},
    {"name": "Cold Hearted", "description": "Use only Frost spells for damage."},
    {"name": "No Wands", "description": "Avoid using wands for ranged attacks."},
    {"name": "No Polymorph", "description": "You cannot use Polymorph to crowd control enemies."},
    {"name": "Naked Mage", "description": "Wear no armor at all."},
    {"name": "No Mana Regen", "description": "You cannot drink water or use any mana-restoration items."},
    {"name": "Close Combat Mage", "description": "Engage every enemy in melee range before attacking."},
    {"name": "1v1 Combat", "description": "Avoid using AoE spells like Blizzard or Arcane Explosion."},
    {"name": "The Unescapist", "description": "You cannot use Frost Nova or Blink to escape or control enemies."},
    {"name": "Wand-Only Caster", "description": "Only use wands for dealing damage."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
    {"name": "Vote of silence", "description": "Do not use the chat while leveling."},
],

"Rogue": [
    {"name": "Lights on", "description": "You cannot use stealth at any time; fight enemies head-on."},
    {"name": "Clean stab", "description": "Do not apply poisons to your weapons."},
    {"name": "Dagger Purist", "description": "Use only daggers for combat."},
    {"name": "Front-stabber", "description": "Do not use positional abilities like Backstab or Ambush."},
    {"name": "Barehanded Rogue", "description": "Fight without any weapons equipped."},
    {"name": "No Gouge or Stuns", "description": "You cannot use Cheap Shot, Gouge, or Kidney Shot."},
    {"name": "Solo Assassin", "description": "Fight only single enemies; avoid cleave or AoE attacks."},
    {"name": "No Healing", "description": "Do not use food, bandages, or potions to heal."},
    {"name": "No Vanish", "description": "You cannot escape fights using Vanish."},
    {"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
],

"Warlock": [
    {"name": "Imp Only", "description": "Only use your imp as your summoned demon. No other demons are allowed."},
    {"name": "Lonely Lock", "description": "You cannot summon or use any demons in combat."},
    {"name": "They Say No Fear", "description": "Fear spells are forbidden."},
    {"name": "Curse Master", "description": "You can only deal damage through curses and damage-over-time abilities."},
    {"name": "DoT and Run", "description": "Use only Damage-over-Time spells and avoid direct damage."},
    {"name": "No Healthstones", "description": "You cannot create or use healthstones for healing."},
    {"name": "Demon Purist", "description": "Focus entirely on Demonology talents and abilities."},
    {"name": "Naked Warlock", "description": "You must wear no armor throughout your journey."},
    {"name": "Barehanded Warlock", "description": "Fight enemies with no weapons equipped, relying on spells only."},
    {"name": "No Shadow Bolt", "description": "Avoid using Shadow Bolt."},
    {"name": "Summoner Warlock", "description": "Your demon must deal all the damage—you cannot attack directly."},
    {"name": "No Soul Shards", "description": "You cannot generate or use Soul Shards for any purpose."},
    {"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
],

"Priest": [
    {"name": "Shadow Purist", "description": "You may only use Shadow spells."},
    {"name": "Holy Purist", "description": "You may only use Holy spells for damage and healing."},
    {"name": "Pacifist Priest", "description": "You can only heal others and cannot deal damage."},
    {"name": "Silence!", "description": "Power Words are off-limits."},
    {"name": "No Healing Spells", "description": "Avoid using any healing spells, including Renew and Heal."},
    {"name": "No Offensive Spells", "description": "You cannot deal damage with spells—use only wands for combat."},
    {"name": "Spirit Ascend", "description": "Prioritize Spirit gear above all other stats."},
    {"name": "No Dispels", "description": "Dispel Magic and Purify cannot be used to remove debuffs."},
    {"name": "Naked Priest", "description": "You may not wear any armor."},
    {"name": "Incompetent", "description": "Do not spend talent points as you level."},
    {"name": "Divine Damage", "description": "Smite is your only offensive ability."},
    {"name": "Shadowform Forever", "description": "Once Shadowform is unlocked, you must remain in it at all times."},
    {"name": "No Wands", "description": "Avoid using wands for combat."},
    {"name": "Purist Buffs", "description": "You can only buff yourself and no other players."},
    {"name": "Wand Specialist", "description": "You can only deal damage with wands."},
    {"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
],

"Druid": [
    {"name": "Bear with me", "description": "You must stay in Bear Form at all times."},
    {"name": "Catception", "description": "You must stay in Cat Form at all times."},
    {"name": "No Shapeshifting", "description": "You cannot use any shapeshifting abilities."},
    {"name": "Balance Purist", "description": "You must focus entirely on Balance spells and talents."},
    {"name": "No Healing Spells", "description": "Avoid using any healing spells, including Rejuvenation and Healing Touch."},
    {"name": "Tanking Druid", "description": "Always act as a tank, even when soloing."},
    {"name": "Pacifist Healer", "description": "Only heal others."},
    {"name": "Hot Hoarder", "description": "You can only heal using healing-over-time abilities like Rejuvenation."},
    {"name": "Nature’s Guardian", "description": "Focus entirely on Nature damage spells."},
    {"name": "No Roots", "description": "You cannot use Entangling Roots or any immobilization abilities."},
    {"name": "Solo Tank", "description": "You must solo level while acting as a tank."},
    {"name": "Rejuvenation Only", "description": "Rejuvenation is your only healing spell."},
    {"name": "Feral Purist", "description": "Focus entirely on Feral talents and avoid Balance and Restoration spells."},
    {"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
],

"Paladin": [
    {"name": "No Seals", "description": "Seals are forbidden; do not cast them."},
    {"name": "Holy Damage", "description": "Focus entirely on Holy spells like Holy Shock for damage."},
    {"name": "No Healing Spells", "description": "Avoid using any healing spells."},
    {"name": "Shieldbearer", "description": "You must always use a shield in combat."},
    {"name": "Retribution Purist", "description": "You must focus entirely on Retribution talents and abilities."},
    {"name": "Tank Paladin", "description": "You must always act as a tank, even while soloing."},
    {"name": "No Lay on Hands", "description": "Lay on Hands is forbidden."},
    {"name": "Naked Paladin", "description": "You cannot wear any armor."},
    {"name": "Aura Specialist", "description": "You must always have an Aura active, prioritizing defensive Auras."},
    {"name": "No Stuns", "description": "Hammer of Justice and other stuns are forbidden."},
    {"name": "Pacifist Paladin", "description": "Avoid fighting whenever possible; focus on healing and buffing others."},
    {"name": "Barehanded Paladin", "description": "Fight without weapons equipped."},
    {"name": "No Consecration", "description": "Avoid using Consecration or any AoE abilities."},
    {"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
],

"Shaman": [
    {"name": "No Totems", "description": "Do not summon or use any totems."},
    {"name": "One Totem Only", "description": "Choose one type of totem (e.g., Earth) and use it exclusively."},
    {"name": "Elemental Purist", "description": "Focus entirely on one element—Earth, Fire, Water, or Air."},
    {"name": "No Healing Spells", "description": "Avoid using any healing spells."},
    {"name": "Melee Purist", "description": "Stick to melee attacks and avoid using spells for damage."},
    {"name": "Caster Shaman", "description": "Focus entirely on casting spells and avoid melee combat."},
    {"name": "No Ghost Wolf", "description": "Do not use Ghost Wolf for movement speed boosts."},
    {"name": "Shield Bearer", "description": "Always equip a shield in combat."},
    {"name": "Barehanded Shaman", "description": "Fight without any weapons equipped."},
    {"name": "No Weapon Imbues", "description": "Avoid using weapon enhancements like Flametongue or Windfury."},
    {"name": "Mana Hoarder", "description": "Keep your mana below 50% at all times."},
    {"name": "Gatherer Shaman", "description": "Only fight mobs while actively gathering resources."},
    {"name": "Totem Purist", "description": "Focus entirely on totem-related talents and abilities."},
    {"name": "No Lightning Spells", "description": "Avoid using Lightning Bolt or Chain Lightning for damage."},
{"name": "Vote of silence", "description": "Do not use the chat while leveling."},
    {"name": "No Bandages", "description": "You cannot use First Aid to heal yourself."},
    {"name": "No Mount", "description": "Walk everywhere, even after level 40."},
    {"name": "No Gear Buffs", "description": "You cannot use sharpening stones or similar items on your gear."},
],

    # Repeat the same structure for all other classes...
}
# Define available professions
professions = [
    "Alchemy",
    "Blacksmithing",
    "Enchanting",
    "Engineering",
    "Herbalism",
    "Leatherworking",
    "Mining",
    "Skinning",
    "Tailoring"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Randomly select a race and valid class
    selected_race = random.choice(list(race_classes.keys()))
    valid_classes = race_classes[selected_race]
    selected_class = random.choice(valid_classes)

    # Check if the user wants a challenge
    include_challenge = request.form.get("include_challenge") == "yes"

    # Generate challenge only if the checkbox is checked
    challenge_name = None
    challenge_description = None
    if include_challenge:
        valid_challenges = class_challenges[selected_class]
        selected_challenge = random.choice(valid_challenges)
        challenge_name = selected_challenge["name"]
        challenge_description = selected_challenge["description"]

    # Randomly select two professions
    selected_professions = random.sample(professions, 2)
    first_profession, second_profession = selected_professions

    # Get avatars
    race_avatar = race_avatars[selected_race]
    class_avatar = class_avatars[selected_class]
    first_profession_avatar = profession_avatars[first_profession]
    second_profession_avatar = profession_avatars[second_profession]

    # Prepare Reddit share URL
    reddit_title = f"{selected_race} {selected_class} - WoW Hardcore Challenge"
    reddit_body = f"""
{selected_race} {selected_class}
Challenge: {challenge_name if challenge_name else 'No Challenge Selected'}
Description: {challenge_description if challenge_description else 'N/A'}
Professions: {first_profession} and {second_profession}
    """.strip()
    reddit_url = "https://www.reddit.com/submit?" + urlencode({"title": reddit_title, "text": reddit_body})

    return render_template(
        "index.html",
        race=selected_race,
        race_avatar=race_avatar,
        class_=selected_class,
        class_avatar=class_avatar,
        challenge_name=challenge_name,
        challenge_description=challenge_description,
        first_profession=first_profession,
        first_profession_avatar=first_profession_avatar,
        second_profession=second_profession,
        second_profession_avatar=second_profession_avatar,
        reddit_url=reddit_url
    )


if __name__ == "__main__":
    app.run(debug=True)