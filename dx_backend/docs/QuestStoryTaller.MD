# Story Builder

The Game Master Tool that helps you build your own stories and quests.

## Story

```
{
    "title": "string",
    "description": "string",
    "tags": ["string", "string", "string"],
    "chapters": []
    "image": "ImageField", // Optional, image file representing the story
    "canonical": true, // Default to false, need review by the Owner
}
```

## Chapter

```
{
    "title": "Chapter 1: The Call to Adventure",
    "description": "The hero receives a mysterious letter that leads them to the first clue of the treasure.",
    "quests": []
    "image": "ImageField", // Optional, image file representing the chapter
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
    "image": "ImageField", // Optional, image file representing the quest
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
    "npc": "uuid", // Optional, if the trigger is related to an CharacterTemplate (all NPCs that belong to this template will be considered)
}
```

## Reward

```
{
    description: "string",
    experience: 100,
    items: [
        {
            "id": "uuid",
            "amount": 1,
            "item": "uuid", // Item reference
            "reward": "uuid" // Reward reference
        }
    ],
    tokens: [
        {
            "id": "uuid",
            "amount": 1,
            "token": "uuid", // Token reference
            "reward": "uuid" // Reward reference
        }
    ],
    effects: [
        {
            "id": "uuid",
            "effect": "uuid", // Effect reference
            "duration": 5, // Duration in turns
            "reward": "uuid" // Reward reference
        }
    ]
}
```

## Note

```
{
    "id": "uuid",
    "quest": "uuid", // Quest reference
    "image": "ImageField", // Optional image file
    "content": "string",
    "order": 0 // Order within the quest
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
                                    "npc": "02119255-181b-48ce-a7c0-e1c255f7db06",
                                    "description": "Follow Brick 'The Boulder' Malone who claims to know about the Ale of Eternity"
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
                                    "npc": "0ee89929-2246-4d56-b598-e53fb3e979a0",
                                    "description": "Defeat Jimmy 'Sparky' Sparks in the ambush"
                                },
                                {
                                    "type": "kill",
                                    "npc": "09bdcdcb-c642-43c0-8dc7-5894315a6257",
                                    "description": "Defeat Ziggy 'Madcap' Malone in the ambush"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've survived the ambush and learned that finding the Ale of Eternity won't be easy. The punk's information might still be valuable.",
                        "experience": 100,
                        "items": [
                            {
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "npc": "a24fa4a7-a1b5-4800-abc0-1d264adfa657",
                                    "description": "Convince Axel Steelguard to let you into restricted areas"
                                },
                                {
                                    "type": "useItem",
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
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "npc": "703a8933-42c5-419e-b720-5c4a491a52f2",
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
                                    "item": "36c78e46-26bb-41ee-a060-d602b1333939",
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
                                "itemId": "da4d21cc-35cd-448f-9792-142dc6fab715",
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
                                    "npc": "75fa20bf-7b1c-4754-aaf4-e11d70600a18",
                                    "description": "Examine the drunk adventurer Finn Barrelstride"
                                }
                            ]
                        }
                    ],
                    "objectives": [
                        {
                            "type": "any",
                            "triggers": [
                                {
                                    "type": "useSkill",
                                    "description": "Steal Finn's mug without waking him"
                                },
                                {
                                    "type": "interaction",
                                    "npc": "75fa20bf-7b1c-4754-aaf4-e11d70600a18",
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
                                "itemId": "41a70083-7403-4e65-83fb-5ca286f758c3",
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
                                    "item": "da4d21cc-35cd-448f-9792-142dc6fab715",
                                    "description": "Use the cryptor to unlock the basement door"
                                },
                                {
                                    "type": "useSkill",
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
                                "tokenId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                    "description": "Help Dr. Elias Thorne find his scattered research team members who were attacked by mercenaries.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "npc": "a1a5929f-d562-41e6-a95e-3fc7ee080fe1",
                                    "description": "Meet Dr. Elias Thorne and learn about his missing team"
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
                                    "npc": "085e0195-895f-44a0-85a8-e7c1704df709",
                                    "description": "Find and rescue Victor Raines"
                                },
                                {
                                    "type": "interaction",
                                    "npc": "2ad47bca-647c-4131-8b2b-eaf71af22479",
                                    "description": "Find and rescue Lucian Vale"
                                },
                                {
                                    "type": "interaction",
                                    "npc": "030ae251-5c93-4dc5-9bb4-f75be07b52fd",
                                    "description": "Find and help wounded Isabelle Orwin"
                                },
                                {
                                    "type": "interaction",
                                    "npc": "398f2346-47b2-493b-9112-7d3ae640a8dc",
                                    "description": "Rescue Sophia Castor from the mercenaries"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully reunited Dr. Thorne's team. They're grateful and offer their expertise to help with your quest.",
                        "experience": 200,
                        "items": [
                            {
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
                                "quantity": 1
                            },
                            {
                                "itemId": "2f50efc5-ea95-4527-bc56-cb2c0b63e0d5",
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
                                    "npc": "9dbca4ce-d5c3-4cad-a512-16baa68b60e3",
                                    "description": "Speak with Captain Aria Steelborne about the incident"
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
                                    "npc": "1790c68e-e4cd-400d-8c8e-c3d02fdfa583",
                                    "description": "Eliminate infected mercenaries"
                                },
                                {
                                    "type": "kill",
                                    "npc": "2dc53aaa-1775-45f8-9a1b-cb16e47adddf",
                                    "description": "Eliminate infected mercenaries"
                                },
                                {
                                    "type": "kill",
                                    "npc": "a55266bc-3b26-4a58-8077-1cebf2259c47",
                                    "description": "Eliminate infected mercenaries"
                                },
                                {
                                    "type": "search",
                                    "item": "f7f61214-5251-4992-9a57-26593a826435",
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
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "npc": "3311a634-adcc-46c0-91e8-2fb2a43fe497",
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
                                    "npc": "3311a634-adcc-46c0-91e8-2fb2a43fe497",
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
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                    "description": "Help the eccentric Flow Guardian Maximus find his lost cyber dog in the dangerous underground.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "npc": "f5533468-0552-470f-a4c8-007c242071df",
                                    "description": "Meet Maximus, the eccentric Flow Guardian"
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
                                    "npc": "15020329-1d9a-4050-af2e-f1eae348cde9",
                                    "description": "Find and safely approach the Cyberhound"
                                },
                                {
                                    "type": "useSkill",
                                    "description": "Use animal handling skills to calm the Cyberhound"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully reunited Maximus with his Cyberhound. The grateful Flow Guardian offers his protection.",
                        "experience": 100,
                        "items": [
                            {
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
                                "quantity": 1
                            }
                        ],
                        "tokens": []
                    },
                    "onFailure": {
                        "description": "The Cyberhound remains hostile or lost. Maximus is disappointed but not angry.",
                        "experience": 25,
                        "items": [],
                        "tokens": []
                    },
                    "cycleLimit": 30
                },
                {
                    "title": "Drake's Mysterious Mission",
                    "description": "Meet with Drake Ironshade, the mercenary leader, and learn about the mysterious expedition that caused the infection.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "npc": "c9e6b8e7-51d4-4579-ba9a-fb1af87da038",
                                    "description": "Meet Drake Ironshade after passing Captain Aria"
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
                                    "npc": "c9e6b8e7-51d4-4579-ba9a-fb1af87da038",
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
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                    "description": "Encounter Kael 'Frostfang' Venir, one of the dangerous Soul Reapers, and avoid conflict if possible.",
                    "starters": [
                        {
                            "type": "all",
                            "triggers": [
                                {
                                    "type": "interaction",
                                    "npc": "7434d0db-4790-4406-bfe7-be6d08fdd8f2",
                                    "description": "Encounter Kael 'Frostfang' Venir the Soul Reaper"
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
                                    "npc": "7434d0db-4790-4406-bfe7-be6d08fdd8f2",
                                    "description": "Avoid conflict by having no artifacts"
                                },
                                {
                                    "type": "kill",
                                    "npc": "7434d0db-4790-4406-bfe7-be6d08fdd8f2",
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
                                    "npc": "d531b1a0-07fb-455b-9342-b2045bd28ef2",
                                    "description": "Meet Vito Ashenvale the rich merchant"
                                },
                                {
                                    "type": "interaction",
                                    "npc": "b89d6d5d-76f1-4769-8d9a-ec46e48268c7",
                                    "description": "Meet Ember Flareheart of the Blood Hunters"
                                },
                                {
                                    "type": "interaction",
                                    "npc": "b0d90aa6-4d34-46ac-ad1b-f5211d708d75",
                                    "description": "Meet Selena Veilforge of the Magician trio"
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
                                    "npc": "d531b1a0-07fb-455b-9342-b2045bd28ef2",
                                    "description": "Choose to help Vito escape safely"
                                },
                                {
                                    "type": "kill",
                                    "npc": "d531b1a0-07fb-455b-9342-b2045bd28ef2",
                                    "description": "Choose to eliminate Vito for the Blood Hunters"
                                },
                                {
                                    "type": "kill",
                                    "npc": "b89d6d5d-76f1-4769-8d9a-ec46e48268c7",
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
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "npc": "f1d85cd6-9793-491c-9e3c-dca44dbf701b",
                                    "description": "Meet Aegis Prime, the friendly android"
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
                                    "npc": "9b9a6710-6cf8-4ab0-86bc-f93b5b97de56",
                                    "description": "Eliminate hostile Zeus Prime androids"
                                },
                                {
                                    "type": "kill",
                                    "npc": "2be12ccb-96df-4bd1-9a2a-6db0a728bac0",
                                    "description": "Eliminate hostile Zeus Prime androids"
                                },
                                {
                                    "type": "interaction",
                                    "description": "Reach the mainframe and stop the Mother AI"
                                }
                            ]
                        }
                    ],
                    "onSuccess": {
                        "description": "You've successfully stopped the Mother AI with Aegis Prime's help. The android threat is neutralized.",
                        "experience": 200,
                        "items": [
                            {
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
                                "quantity": 1
                            },
                            {
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "item": "ec43868c-7318-4563-bf1a-8909fd09e6a3",
                                    "description": "Use protection runes from Drake Ironshade"
                                },
                                {
                                    "type": "useItem",
                                    "item": "e6e9dd8b-ba1b-44f4-9df7-e2bc0567da57",
                                    "description": "Use repaired scuba gear from Dr. Thorne"
                                },
                                {
                                    "type": "search",
                                    "item": "2f50efc5-ea95-4527-bc56-cb2c0b63e0d5",
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
                                "itemId": "2f50efc5-ea95-4527-bc56-cb2c0b63e0d5",
                                "quantity": 1
                            },
                            {
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "item": "2f50efc5-ea95-4527-bc56-cb2c0b63e0d5",
                                    "description": "Use the ancient artifact with the gate"
                                },
                                {
                                    "type": "interaction",
                                    "npc": "a1a5929f-d562-41e6-a95e-3fc7ee080fe1",
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
                                "itemId": "e1a76f41-2688-465f-89a6-2b6f45a87045",
                                "quantity": 1
                            }
                        ],
                        "tokens": [
                            {
                                "tokenId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "npc": "41a9ff41-214b-43a8-bc84-27792162dd52",
                                    "description": "Successfully negotiate with Cablo for a portion of the Ale"
                                },
                                {
                                    "type": "kill",
                                    "npc": "41a9ff41-214b-43a8-bc84-27792162dd52",
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
                                "itemId": "36c78e46-26bb-41ee-a060-d602b1333939",
                                "quantity": 1
                            }
                        ],
                        "tokens": [
                            {
                                "tokenId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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
                                    "item": "36c78e46-26bb-41ee-a060-d602b1333939",
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
                                "itemId": "33b71c99-53b1-4759-81a3-39312e3794eb",
                                "quantity": 1
                            }
                        ],
                        "tokens": [
                            {
                                "tokenId": "33b71c99-53b1-4759-81a3-39312e3794eb",
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