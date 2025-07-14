# Story Builder

The Game Master Tool that helps you build your own stories and quests.

## Story

```
{
    "title": "string",
    "description": "string",
    "tags": ["string", "string", "string"],
    "chapters": []
    "image": "string", // Optional, URL to an image representing the story
    "canonical": true, // Default to false, need review by the Owner
}
```

## Chapter

```
{
    "title": "Chapter 1: The Call to Adventure",
    "description": "The hero receives a mysterious letter that leads them to the first clue of the treasure.",
    "quests": []
    "image": "string", // Optional, URL to an image representing the chapter
}
```

## Quest

```
{
    "title": "string",
    "description": "string",
    "starters": [
        Condition{}
    ],
    "objectives": [
        Condition{}
    ],
    "onSuccess": Reward{},
    "onFailure": Reward{},
    "image": "string", // Optional, URL to an image representing the quest
    "cycleLimit": 50, // Optional, time limit in cycles (1 cycle = 1 turn)
}
```

## Condition

```
{
    "type": "Enum(all, any, none)",
    "triggers": [
        Trigger{}
    ],
}
```

## Trigger

```
{   
    "type": "Enum(search, kill, interaction, position, useItem, useSkill)",
    "gameObject": "uuid" // Item, NPC, Anomaly
    "position": "uuid", // Position in the game world
    "description": "string",
    "location": "uuid", // Optionaly Limit trigger to a specific location
}
```

## Reward

```
{
    description: "string",
    items: [
        {
            "itemId": "uuid",
            "quantity": 1
        }
    ],
    tokens: [
        {
            "tokenId": "uuid",
            "quantity": 1
        }
    ],
    experience: 100,
}
```

# [!] SPOILERS ALERT [!]

### Story: Ale of Eternity

#### Chapter 1 - The Call to Adventure

- The characters receive a mysterious letter that leads them to arrive to the City of Memories.
- Then meet niar the Monument an meath each other test game mechanics and undertand game rules.
- They meet Valid Arbiter, a mysterious figure who say about te world and dissapear.
- Then need to find the Ale of Eternity, a legendary drink. [Main Quest for the story]
- They could inbbestigate the city and meet their first NPCs
- Punk say that he knows where the Ale of Eternity is, but we need to fillow him near by the bar.
- Jimmy Brick and Zigge wait in ambush to ambush the characters, they are punks and want to steal the maney.
- Eira Is the master of Path of JSon shi could advise or reset stats for the Path of JSon.
- Derreikk Auger is master of the Path of Jhohn, he could reset stats or give advice for the Path of John.
- The Axel security don't seem to be very friendly, he never seen us before and he is not happy about it, need to find a
  way to convince him to let us in.
- The Calvin Drift is ex flow-guardian, now hi is just a drunkard, but he know how to reach the basemant of Misfits Pub,
  but he need 2 cups of the Misfits Best Ale as a reword he give you you the cryptor that could open the dour behinde
  him
- The Nancy is the waitress of the Misfits Pub, shi is pretty and super fast, she could give you some information about
  the city and the people in it. Also She could give you a drink, but you need to pay for it.
- The Alex the bartender is a grumpy tuff person, he don't like strangers and he don't like to talk he is lonely sittin
  behind the bar, but he could give you a drink if you pay for it or if you convince him to do it for example by winning
  in arm wrestling.
- Nancy Alex and Axel have key to the Misfits Pub that opens all doors including the private restroom.
- Finn is durnk to death, he is a top grade adventurer, but now he is just a drunkard, you can see tha glowing liquid in
  his mug looks like it was Ale of Eternity, but it's empty now, you can stole his mug, but he will not be happy about
  it when he wake up.
- Also there the hidden path that closed by the luck cap, you need to have the gear to open it or dice 20 with at least
  15 of power to open it.
- So The chapter 1 ends when the characters reach the basement of the Misfits Pub

#### Chapter 2 - Exlporation of the Misfits Pub Underworld

- The characters reach the basement of the Misfits Pub, there is a lot of strange things here, but they need to find the
  Ale of Eternity.
- The adventure understand that it's quirte dangerous here, so they need to be careful and find some safe place to
  rest.
- Dr. Elies Thorne is a scientist who is studying the Misfits Pub Underworld he with the group of scientists is trying
  to
  find the Entient Library that by the taks from some wery reach organization that hi refuse to name. The problem is
  they was attacked by the mercinaries and there were something strage in thaer ees
- Now the Dr. Elies Thorne is alone and he want we to help him to find the rest of his team.
- Victor Raines is part of the Dr. Elies Thorne team, he is an security that basically faked his skill to make easy
  mones as the undergoun seems easy target, but now he is in trouble and need help.
- Lucian Vaile the great engeener of flow tech he could make some repairs and upgrades, he lost but he is still alive,
  he afraid of any mercenary and he is hiding in the safe place.
- Isabelle Orwin the great medic of the Dr. Elies Thorne team, she is wounded and need help, but she is still alive.
- Sofia Caster the great hacker of the Dr. Elies Thorne team, she was captured by the mercenaries and now shis lifes in
  thair hands, but she is still alive.
- Also Character could face the Glowing Rat like creature he looks friendly and if somebody understand the flow
  creatures they could talk to him, his name is Rynak and he warnk about the death and danger that if you hear the rats
  run away as fast as you can.
- The Maximys is the Flow Guardian who was walking with his dog to play, hi is 100% nut but 100% strong and friendly, he
  stink is good idea to play with the dog here but when thay faced mercenaries the dog war run away and Maximys is angry
  and he want to find his dog.
- The dog Cyberhound is a cyber dog that was lost in the Misfits Pub Underworld, it's not friendly anb strong it attaks
  anybody who is not Maximys or don't know how to talk to him, but he is not dangerous if you know how to talk to him.
- Capitan Aria is the leader of the mercenaries security team, she don't allow you to pass the camp becouse of the
  incendent, she don't mention the details of the indenent, you need to find a way to convince her to let you pass.
- The mad merks are the mercenaries who are spread for the Misfits Pub Underworld, they are not friendly and thay looks
  like some virus infected, they eyes are glowing and they are very dangerous, but they are not very smart becose of the
  virus.
- When you faced this mad merks you understand that this is about the indent that Capitan Aria mentioned, you need to
  find out what happened and how to stop it.
- If You return to the Aria and tell her about the mad merks she woun't left you pass, until you elliminate the mad
  merks and gahter at list 5 items as evidence - damaged weapons, broken armor.
- When you had enough evidence you can return to the Aria and she still not happy that merks died, but she let you pass.
- Incide you find Drake Ironhande this is the leader of the mercenaries, you could trade with him, and he could say that
  the ingury was caused by the expidition to the down level of the basement, but he don't know what happened there, he
  just warned us not to go there. He can't say what was the mission of the merks, but if you go there and if you find
  `that` you will understand when you see it, just bring this to me you would be reworder.
- Kael is one of Soul Reapers, he is a very dangerous and powerful he is neutral to you, he seek for the artifacts, and
  if you have some hi wold definitely attack you, but if you don't have any artifacts he will just leave you alone.
- The chapter 2 ends when the characters reach the down level of the Misfits Pub Underworld.

#### Chapter 3 - The Down Level of the Misfits Pub Underworld

- The Vito The reach merchant is the leader of the Vito's gang, he friendly and he had no clue how he ended up here, he
  appritiate is somenone help him to get out of here.
- Ember Flame Hart one of the Blood Hunters, looks pretty but don't be fooled by her beauty, shi seek for a Vito and
  want to have his head.
- Liric Dawnshade is not a lucky adventurer, he is a good guy but he is not very smart, he is just trying to survive
  here. Appritiate heal and food.
- Titan fucking is a big guy who is not very smart but he is very strong, he is not friendly and he is not happy that
  you are here.
- Kael Vortex the flow guardian, insaint and dangerous, he is not friendly and he is not happy that you are here, but he
  is not attacking you, he just watching you, don't look in his eyes don't talk to him don't touch him, just leave him
  alone.
- The trio Makrick, Elyra and Kaeken is Blood Hunters, thy just wait for thar friend Ember Flame Hart to return, they
  approach you and ask to bring Vito's head to them and then they finally can leave this fucking place. If you dial with
  the Magicians they will attack you, if you free Vito they will attack you.
- The trio Selena, Orlin Laelion is Magicans thay was aimed to find and survive the Vito. If you make a dial with Blood
  Hunters they will attack you, if you kill Vito they will attack you.
- The Vailder Keeperer is a powerful and dangerous creature, he have a shop and he could trade with you, but he don't
  talk at all.
- The Library Gate is a mysterious and antient gate mechanism, it looks like it could be opened by the flow, but you
  need to find the key and the instructions how to open it. Require the team of scientists to open it. And the antient
  artifact that could be found in the Misfits Pub Underworld.
- The Black Whater is like regular liquid, but it is not, it is a flow created one, it's killing you slowly by sucking
  your life energy, you need to find a way to stop this effect.
- Some flooded flour was found under the Black Water, there could be some interesting things in it, but you need to find
  a way to stop the Black Water effect and get the geat to breath under the water.
- When you find the artifact you need to return it to the Merks leader Drake Ironhande, and he would be happy give you
  protection runes that could protect you from the Black Water.
- The chpaters of scuba you can find in the undergraund you need the Dr. Elies Thorne to make the repairs and upgrades,
  he could do it for the flow crystals.
- Zheus Prime 00 Is Android class that is controlled by the eavil AI, teay spreaded by the dungion and attack you and
  any alive non metalic crature, you need to find a way to stop them.
- Zheus Prime 01 Is Android class that was break the AI control and now he is friendly to you, he could help you to find
  the way to stop the Zheus Prime 00 and the Mother AI.
- When characte facedf the Zheus thay had the understanding that the Zheus Prime 00 is controlled by the Mother AI, and
  they need to find a way to stop it.
- The mainframe is the place where the Mother AI is located, you need to find a way to reach it and stop it with helo of
  the Zheus Prime 01.
- The chapter 3 ends when the characters find the right whay to underwather and reach the hidden Hall

#### Chapter 4 - The Hidden Hall

- Cablo the flow creature is super big and stong is boss of the Hidden Hall, he is taking a nap on his throne
- In this hall could be grat battle or dialogue with Cablo, the cablo is hilder of the Ale of Eternity, but he is not
  happy that you are here, and want his Ale of Eternity
- Characters could try to convince Cablo to give them the part of his Ale of Eternity or fight with him and take it by
  force.
- The chapter ends when the characters get the Ale of Eternity

Main Quest Ends

The character have a party with or vithout Cablo.

## Structure Example

```
{
    "title": "Ale of Eternity",
    "description": "A legendary quest to find the mystical Ale of Eternity, beginning in the City of Memories and descending through dangerous underground realms filled with ancient secrets, hostile creatures, and powerful artifacts.",
    "tags": ["adventure", "mystery", "underground", "artifact_hunt", "team_building"],
    "image": "https://example.com/ale_of_eternity_cover.jpg",
    "canonical": true,
    "chapters": [
        {
            "title": "Chapter 1: The Call to Adventure",
            "description": "The heroes arrive in the City of Memories following a mysterious letter, meet each other near the Monument, and begin their search for the legendary Ale of Eternity while navigating the social dynamics of the Misfits Pub.",
            "image": "https://example.com/chapter1_city_of_memories.jpg",
            "quests": [
                {
                    "title": "Arrival at the Monument",
                    "description": "Meet other adventurers near the Monument in the City of Memories and learn about the world.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "position",
                                    "position": "monument_city_of_memories",
                                    "description": "Arrive at the Monument in City of Memories"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "valid_arbiter_npc",
                                    "description": "Speak with Valid Arbiter about the world",
                                    "location": "monument_area"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've learned the basics of the world and met your fellow adventurers. Valid Arbiter has disappeared, leaving you with cryptic knowledge.",
                        "experience": 50,
                        "items": [],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "You missed the opportunity to learn from Valid Arbiter.",
                        "experience": 0,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 20
                },
                {
                    "title": "The Ale of Eternity Quest Begins",
                    "description": "Learn about the legendary Ale of Eternity and begin your search. A punk claims to know its location.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "punk_npc",
                                    "description": "Follow the punk who claims to know about the Ale of Eternity"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "kill",
                                    "gameObject": "jimmy_brick_npc",
                                    "description": "Defeat Jimmy Brick in the ambush"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "zigge_npc",
                                    "description": "Defeat Zigge in the ambush"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've survived the ambush and learned that finding the Ale of Eternity won't be easy. The punk's information might still be valuable.",
                        "experience": 100,
                        "items": [
                            {
                                "itemId": "punk_information_token",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "The ambush proved too difficult. You'll need to find another way to learn about the Ale of Eternity.",
                        "experience": 25,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 30
                },
                {
                    "title": "Gaining Access to Misfits Pub",
                    "description": "Navigate the social dynamics of the Misfits Pub to gain access to restricted areas. Deal with Axel the security guard and gather information from the staff.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "position",
                                    "position": "misfits_pub_entrance",
                                    "description": "Approach the Misfits Pub"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "axel_security_npc",
                                    "description": "Convince Axel to let you into restricted areas"
                                },
                                {
                                    "type": "useItem",
                                    "gameObject": "misfits_pub_key",
                                    "description": "Use a key obtained from Nancy, Alex, or Axel"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've gained access to the Misfits Pub's restricted areas. The path to the basement is now open.",
                        "experience": 75,
                        "items": [
                            {
                                "itemId": "basement_access_token",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "Access denied. You'll need to find another way into the restricted areas.",
                        "experience": 10,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 40
                },
                {
                    "title": "The Cryptor Key",
                    "description": "Obtain the cryptor from Calvin Drift to open the door behind him. He requires 2 cups of Misfits Best Ale as payment.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "calvin_drift_npc",
                                    "description": "Speak with Calvin Drift about accessing the basement"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "useItem",
                                    "gameObject": "misfits_best_ale",
                                    "description": "Give Calvin 2 cups of Misfits Best Ale",
                                    "location": "misfits_pub"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "Calvin hands over the cryptor with a knowing smile. The door to the basement is now unlocked.",
                        "experience": 60,
                        "items": [
                            {
                                "itemId": "basement_cryptor",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "Calvin remains stubborn. You'll need to find another way to access the basement.",
                        "experience": 5,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 25
                },
                {
                    "title": "Finn's Empty Mug",
                    "description": "Investigate Finn, the drunk adventurer, and his mysterious empty mug that once contained what appears to be Ale of Eternity.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "finn_npc",
                                    "description": "Examine the drunk adventurer Finn"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "useItem",
                                    "gameObject": "stealth_skill",
                                    "description": "Steal Finn's mug without waking him"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "finn_npc",
                                    "description": "Wake Finn and ask about the mug"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You obtain Finn's mug, which still has traces of a glowing substance. This could be a valuable clue about the Ale of Eternity.",
                        "experience": 40,
                        "items": [
                            {
                                "itemId": "finns_mug",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "Your attempt failed. Finn might be more alert than he appears.",
                        "experience": 10,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 15
                },
                {
                    "title": "Reach the Basement",
                    "description": "Successfully navigate all obstacles and reach the basement of the Misfits Pub, beginning your underground adventure.",
                    "starters": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "useItem",
                                    "gameObject": "basement_cryptor",
                                    "description": "Use the cryptor to unlock the basement door"
                                },
                                {
                                    "type": "useSkill",
                                    "gameObject": "lock_picking_skill",
                                    "description": "Pick the lock (requires dice roll 15+ with power)"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "position",
                                    "position": "misfits_pub_basement",
                                    "description": "Enter the Misfits Pub basement"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully entered the basement of the Misfits Pub. The underground world awaits, full of dangers and mysteries.",
                        "experience": 100,
                        "items": [],
                        "tokens": [
                            {
                                "tokenId": "chapter_1_completion",
                                "quantity": 1
                            }
                        ]
                    },
                    "onFailure": {
                        "description": "The basement remains sealed. You'll need to find another approach.",
                        "experience": 20,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 10
                }
            ]
        },
        {
            "title": "Chapter 2: Exploration of the Misfits Pub Underworld",
            "description": "The heroes descend into the dangerous basement levels, encountering Dr. Elies Thorne's scattered research team, mad mercenaries infected by a mysterious virus, and various underground creatures while searching for clues about the Ale of Eternity.",
            "image": "https://example.com/chapter2_underworld.jpg",
            "quests": [
                {
                    "title": "Rescue Dr. Thorne's Team",
                    "description": "Help Dr. Elies Thorne find his scattered research team members who were attacked by mercenaries.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "dr_elies_thorne_npc",
                                    "description": "Meet Dr. Elies Thorne and learn about his missing team"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "victor_raines_npc",
                                    "description": "Find and rescue Victor Raines"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "lucian_vaile_npc",
                                    "description": "Find and rescue Lucian Vaile"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "isabelle_orwin_npc",
                                    "description": "Find and help wounded Isabelle Orwin"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "sofia_caster_npc",
                                    "description": "Rescue Sofia Caster from the mercenaries"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully reunited Dr. Thorne's team. They're grateful and offer their expertise to help with your quest.",
                        "experience": 200,
                        "items": [
                            {
                                "itemId": "team_gratitude_token",
                                "quantity": 1
                            },
                            {
                                "itemId": "research_notes",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "Some team members remain missing. Dr. Thorne is distraught but still offers limited help.",
                        "experience": 100,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 50
                },
                {
                    "title": "The Mad Merks Investigation",
                    "description": "Investigate the mysterious virus affecting the mercenaries and gather evidence for Captain Aria.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "captain_aria_npc",
                                    "description": "Speak with Captain Aria about the incident"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "kill",
                                    "gameObject": "mad_merk_1",
                                    "description": "Eliminate infected mercenaries"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "mad_merk_2",
                                    "description": "Eliminate infected mercenaries"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "mad_merk_3",
                                    "description": "Eliminate infected mercenaries"
                                },
                                {
                                    "type": "search",
                                    "gameObject": "damaged_weapon_evidence",
                                    "description": "Collect at least 5 pieces of evidence"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've eliminated the infected mercenaries and gathered sufficient evidence. Captain Aria reluctantly allows you to pass.",
                        "experience": 150,
                        "items": [
                            {
                                "itemId": "passage_permission",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "Insufficient evidence or failure to eliminate the threat. Captain Aria blocks your passage.",
                        "experience": 50,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 40
                },
                {
                    "title": "Rynak's Warning",
                    "description": "Encounter Rynak, the friendly glowing rat creature, and heed his warning about the dangers ahead.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "rynak_npc",
                                    "description": "Meet the glowing rat creature Rynak"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "rynak_npc",
                                    "description": "Listen to Rynak's warning about danger"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "Rynak warns you about impending danger: 'When you hear the rats run, run away as fast as you can!' This knowledge may save your life.",
                        "experience": 50,
                        "items": [
                            {
                                "itemId": "rynaks_warning",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "You failed to understand Rynak's warning. You'll face future dangers unprepared.",
                        "experience": 10,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 15
                },
                {
                    "title": "Maximys and the Lost Cyberhound",
                    "description": "Help the eccentric Flow Guardian Maximys find his lost cyber dog in the dangerous underground.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "maximys_npc",
                                    "description": "Meet Maximys, the eccentric Flow Guardian"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "cyberhound_npc",
                                    "description": "Find and safely approach the Cyberhound"
                                },
                                {
                                    "type": "useSkill",
                                    "gameObject": "animal_handling_skill",
                                    "description": "Use animal handling skills to calm the Cyberhound"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully reunited Maximys with his Cyberhound. The grateful Flow Guardian offers his protection.",
                        "experience": 100,
                        "items": [
                            {
                                "itemId": "maximys_blessing",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "The Cyberhound remains hostile or lost. Maximys is disappointed but not angry.",
                        "experience": 25,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 30
                },
                {
                    "title": "Drake's Mysterious Mission",
                    "description": "Meet with Drake Ironhande, the mercenary leader, and learn about the mysterious expedition that caused the infection.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "drake_ironhande_npc",
                                    "description": "Meet Drake Ironhande after passing Captain Aria"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "drake_ironhande_npc",
                                    "description": "Learn about the expedition to the lower levels"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "Drake reveals that the infection was caused by an expedition to the lower levels. He promises a reward if you bring back 'that thing' - you'll know it when you see it.",
                        "experience": 75,
                        "items": [
                            {
                                "itemId": "drakes_mission",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "Drake remains secretive about the expedition details.",
                        "experience": 20,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 20
                },
                {
                    "title": "Kael the Soul Reaper",
                    "description": "Encounter Kael, one of the dangerous Soul Reapers, and avoid conflict if possible.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "kael_soul_reaper_npc",
                                    "description": "Encounter Kael the Soul Reaper"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "kael_soul_reaper_npc",
                                    "description": "Avoid conflict by having no artifacts"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "kael_soul_reaper_npc",
                                    "description": "Defeat Kael if he attacks"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully navigated the encounter with Kael. Whether through avoiding conflict or defeating him, you've survived one of the underground's most dangerous inhabitants.",
                        "experience": 120,
                        "items": [],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "The encounter with Kael went poorly. You've learned the hard way about the Soul Reapers.",
                        "experience": 30,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 25
                }
            ]
        },
        {
            "title": "Chapter 3: The Down Level of the Misfits Pub Underworld",
            "description": "The heroes reach the deeper underground levels where they encounter gang conflicts, android threats controlled by an evil AI, navigate the deadly Black Water, and prepare for the final descent to the Hidden Hall.",
            "image": "https://example.com/chapter3_down_level.jpg",
            "quests": [
                {
                    "title": "The Gang Conflict",
                    "description": "Navigate the complex conflict between Vito's gang, the Blood Hunters seeking his head, and the Magicians protecting him.",
                    "starters": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "vito_merchant_npc",
                                    "description": "Meet Vito the rich merchant"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "ember_flame_hart_npc",
                                    "description": "Meet Ember Flame Hart of the Blood Hunters"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "selena_magician_npc",
                                    "description": "Meet the Magician trio"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "vito_merchant_npc",
                                    "description": "Choose to help Vito escape safely"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "vito_merchant_npc",
                                    "description": "Choose to eliminate Vito for the Blood Hunters"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "ember_flame_hart_npc",
                                    "description": "Choose to fight the Blood Hunters"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've resolved the gang conflict through your chosen approach. The surviving factions remember your decision.",
                        "experience": 150,
                        "items": [
                            {
                                "itemId": "faction_standing_token",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "The conflict escalated beyond control. Multiple factions are now hostile to you.",
                        "experience": 50,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 45
                },
                {
                    "title": "The Android Uprising",
                    "description": "Deal with the Zeus Prime androids controlled by an evil AI and find a way to stop the Mother AI with the help of Zeus Prime 01.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "zeus_prime_01_npc",
                                    "description": "Meet Zeus Prime 01, the friendly android"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "kill",
                                    "gameObject": "zeus_prime_00_1",
                                    "description": "Eliminate hostile androids"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "zeus_prime_00_2",
                                    "description": "Eliminate hostile androids"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "mainframe_terminal",
                                    "description": "Reach the mainframe and stop the Mother AI"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully stopped the Mother AI with Zeus Prime 01's help. The android threat is neutralized.",
                        "experience": 200,
                        "items": [
                            {
                                "itemId": "ai_core_fragment",
                                "quantity": 1
                            },
                            {
                                "itemId": "zeus_alliance_token",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "The Mother AI remains active. The android threat continues to spread.",
                        "experience": 75,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 40
                },
                {
                    "title": "Navigating the Black Water",
                    "description": "Find a way to cross the deadly Black Water that drains life energy, requiring protection runes and underwater breathing equipment.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "position",
                                    "position": "black_water_area",
                                    "description": "Reach the Black Water area"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "useItem",
                                    "gameObject": "protection_runes",
                                    "description": "Use protection runes from Drake Ironhande"
                                },
                                {
                                    "type": "useItem",
                                    "gameObject": "scuba_gear_repaired",
                                    "description": "Use repaired scuba gear from Dr. Thorne"
                                },
                                {
                                    "type": "search",
                                    "gameObject": "underwater_artifact",
                                    "description": "Find the ancient artifact underwater"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully navigated the Black Water and found the ancient artifact. The path to the Hidden Hall is revealed.",
                        "experience": 180,
                        "items": [
                            {
                                "itemId": "ancient_underwater_artifact",
                                "quantity": 1
                            },
                            {
                                "itemId": "hidden_hall_access",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "The Black Water proves too dangerous. You'll need better preparation to cross safely.",
                        "experience": 40,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 35
                },
                {
                    "title": "The Library Gate",
                    "description": "Help Dr. Thorne's team open the mysterious Library Gate using the ancient artifact and their scientific expertise.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "library_gate_mechanism",
                                    "description": "Examine the ancient Library Gate"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "useItem",
                                    "gameObject": "ancient_underwater_artifact",
                                    "description": "Use the ancient artifact with the gate"
                                },
                                {
                                    "type": "interaction",
                                    "gameObject": "dr_elies_thorne_npc",
                                    "description": "Have Dr. Thorne's team operate the gate"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "The Library Gate opens with a deep rumbling, revealing ancient passages that lead toward the Hidden Hall. Knowledge from a forgotten age beckons.",
                        "experience": 120,
                        "items": [
                            {
                                "itemId": "library_gate_key",
                                "quantity": 1
                            }
                        ],
                        "tokens": [
                            {
                                "tokenId": "chapter_3_completion",
                                "quantity": 1
                            }
                        ]
                    },
                    "onFailure": {
                        "description": "The Library Gate remains sealed. Ancient secrets stay hidden for now.",
                        "experience": 30,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 25
                }
            ]
        },
        {
            "title": "Chapter 4: The Hidden Hall",
            "description": "The heroes reach the final chamber where Cablo, the mighty flow creature, guards the legendary Ale of Eternity. The ultimate test awaits - will they choose diplomacy or force to claim their prize?",
            "image": "https://example.com/chapter4_hidden_hall.jpg",
            "quests": [
                {
                    "title": "The Final Confrontation",
                    "description": "Face Cablo, the guardian of the Ale of Eternity, in the Hidden Hall. Choose between diplomacy and combat to achieve your ultimate goal.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "position",
                                    "position": "hidden_hall_throne_room",
                                    "description": "Enter the Hidden Hall and approach Cablo's throne"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "cablo_npc",
                                    "description": "Successfully negotiate with Cablo for a portion of the Ale"
                                },
                                {
                                    "type": "kill",
                                    "gameObject": "cablo_npc",
                                    "description": "Defeat Cablo in combat and claim the Ale by force"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "Success! You have obtained the legendary Ale of Eternity. Whether through wit or might, your quest is complete. The ancient power flows through the mystical brew.",
                        "experience": 500,
                        "items": [
                            {
                                "itemId": "ale_of_eternity",
                                "quantity": 1
                            }
                        ],
                        "tokens": [
                            {
                                "tokenId": "quest_completion_ale_of_eternity",
                                "quantity": 1
                            }
                        ]
                    },
                    "onFailure": {
                        "description": "Cablo proves too powerful, or your diplomatic efforts fall short. The Ale of Eternity remains beyond your grasp, but wisdom has been gained.",
                        "experience": 200,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 50
                },
                {
                    "title": "The Celebration",
                    "description": "With the Ale of Eternity obtained, celebrate your success with your companions and perhaps even with Cablo, depending on how the confrontation ended.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "useItem",
                                    "gameObject": "ale_of_eternity",
                                    "description": "Use the Ale of Eternity to begin the celebration"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "gameObject": "party_celebration",
                                    "description": "Participate in the victory celebration"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "A magnificent celebration ensues! The Ale of Eternity grants each participant a taste of immortal bliss. Your legend will be told for generations to come.",
                        "experience": 300,
                        "items": [
                            {
                                "itemId": "eternal_blessing",
                                "quantity": 1
                            }
                        ],
                        "tokens": [
                            {
                                "tokenId": "legendary_hero_status",
                                "quantity": 1
                            }
                        ]
                    },
                    "onFailure": {
                        "description": "The celebration is subdued, but the quest's completion still brings satisfaction and closure.",
                        "experience": 100,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 20
                }
            ]
        }
    ]
}
```