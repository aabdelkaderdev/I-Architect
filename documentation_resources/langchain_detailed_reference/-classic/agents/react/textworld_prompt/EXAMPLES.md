<!-- Source: https://reference.langchain.com/python/langchain-classic/agents/react/textworld_prompt/EXAMPLES -->

Attributev1.2.13 (latest)●Since v1.0

# EXAMPLES


```
EXAMPLES = ["Setup: You are now playing a fast paced round of TextWorld! Here is your task for\ntoday. First of all, you could, like, try to travel east. After that, take the\nbinder from the locker. With the binder, place the binder on the mantelpiece.\nAlright, thanks!\n\n-= Vault =-\nYou've just walked into a vault. You begin to take stock of what's here.\n\nAn open safe is here. What a letdown! The safe is empty! You make out a shelf.\nBut the thing hasn't got anything on it. What, you think everything in TextWorld\nshould have stuff on it?\n\nYou don't like doors? Why not try going east, that entranceway is unguarded.\n\nThought: I need to travel east\nAction: Play[go east]\nObservation: -= Office =-\nYou arrive in an office. An ordinary one.\n\nYou can make out a locker. The locker contains a binder. You see a case. The\ncase is empty, what a horrible day! You lean against the wall, inadvertently\npressing a secret button. The wall opens up to reveal a mantelpiece. You wonder\nidly who left that here. The mantelpiece is standard. The mantelpiece appears to\nbe empty. If you haven't noticed it already, there seems to be something there\nby the wall, it's a table. Unfortunately, there isn't a thing on it. Hm. Oh well\nThere is an exit to the west. Don't worry, it is unguarded.\n\nThought: I need to take the binder from the locker\nAction: Play[take binder]\nObservation: You take the binder from the locker.\n\nThought: I need to place the binder on the mantelpiece\nAction: Play[put binder on mantelpiece]\n\nObservation: You put the binder on the mantelpiece.\nYour score has just gone up by one point.\n*** The End ***\nThought: The End has occurred\nAction: Finish[yes]\n\n"]
```


