# Comprehensive list of abuse indicators categorized by type of coercive control
# These keywords are used to scan documents for potential abuse patterns.

ABUSE_INDICATORS = {
    "Isolation": [
        # Original
        "don't talk to", "stay away from", "no friends", "bad influence",
        "don't go out", "who were you with", "where were you", "check your phone",
        "give me your password", "you spend too much time with", "they don't like me",
        "choose them or me", "forbidden", "not allowed", "grounded",
        "cut off", "block them", "delete their number", "why didn't you answer",
        "tracking", "location", "gps", "constantly calling", "texting all the time",
        # Duluth Wheel
        "controlling who you see", "limiting outside involvement", "jealousy", "monitoring calls",
        "making you account for your time", "interrogating your whereabouts", "isolating from support",
        # NDCC Ch. 12
        "restraint", "confinement", "removal from home", "preventing access to services",
        # New slang
        "ghosting", "gaslighting", "breadcrumbing", "orbiting", "love bombing", "dry texting"
        # Expanded
        "cut off from family", "no contact allowed", "can't see your friends", "blocked from social media",
        "forced to move", "not allowed to work", "kept at home", "monitored calls", "monitored texts",
        "no privacy", "read your messages", "read your diary", "spying on you", "hidden cameras",
        "listening devices", "forced to share location", "demanding check-ins", "constant surveillance"
    ],
    "Emotional Abuse / Degradation": [
        "crazy", "stupid", "worthless", "fat", "ugly", "useless",
        "nobody else would want you", "lucky to have me", "it's all your fault",
        "you make me do this", "too sensitive", "can't take a joke", "overreacting",
        "imagining things", "liar", "pathetic", "disgusting", "whore", "slut",
        "cheat", "unfaithful", "brainwashed", "mental", "psycho", "bitch",
        "shut up", "idiot", "incompetent", "failure",
        # Duluth Wheel
        "put-downs", "name-calling", "humiliation", "making you feel guilty",
        "playing mind games", "making you feel crazy", "minimizing abuse",
        # NDCC Ch. 12
        "verbal abuse", "emotional harm", "demeaning language",
        # New slang
        "simp", "pick me", "trash", "clown", "salty", "flexing", "ratioed"
        # Expanded
        "gaslight", "crazy-making", "you're imagining things", "no one believes you", "you're paranoid",
        "you're dramatic", "always your fault", "never good enough", "hopeless", "unlovable",
        "nobody cares", "everyone hates you", "you're a burden", "crybaby", "overly emotional",
        "can't trust you", "you're broken", "damaged", "always wrong", "never right"
    ],
    "Financial Control": [
        "my money", "allowance", "receipts", "how much did you spend",
        "can't afford", "waste of money", "stole", "bank account",
        "credit card", "pin number", "paycheck", "deposit", "sign this",
        "debt", "loan", "owing me", "buying love", "financial support",
        "work", "quit your job", "get a job", "control the finances",
        # Duluth Wheel
        "taking your money", "not letting you work", "making you ask for money",
        "withholding funds", "stealing from you", "ruining your credit",
        # NDCC Ch. 12
        "economic abuse", "financial exploitation", "fraud",
        # New slang
        "sugar daddy", "venmo me", "cash app", "finesse", "scam"
        # Expanded
        "can't have your own account", "no access to money", "forced to hand over paycheck",
        "not allowed to spend", "questioning every purchase", "financial punishment", "withholding necessities",
        "forced to sign loans", "forced debt", "ruined credit", "stolen identity", "forced to beg for money"
    ],
    "Threats / Intimidation": [
        "kill you", "kill myself", "take the kids", "hurt the kids",
        "hurt your family", "destroy", "burn", "break", "smash",
        "hit", "punch", "slap", "kick", "choke", "strangle",
        "weapon", "gun", "knife", "watch your back", "regret it",
        "make you pay", "call the police", "report you", "deport",
        "ruin your reputation", "out you", "tell everyone",
        # Duluth Wheel
        "making you afraid", "threatening to hurt you", "displaying weapons",
        "destroying property", "abusing pets", "stalking",
        # NDCC Ch. 12
        "terrorizing", "menacing", "harassment", "intimidation",
        # New slang
        "dox", "swat", "cancel", "expose", "leak", "drag"
        # Expanded
        "threaten to leave", "threaten to harm pets", "threaten to ruin career", "threaten to expose secrets",
        "threaten to call cps", "threaten to get custody", "threaten to hurt themselves", "threaten to hurt you",
        "threaten to make you homeless", "threaten to get you fired", "threaten to ruin your life"
    ],
    "Sexual Coercion": [
        "owe me", "if you loved me", "don't be a prude", "frigid",
        "duty", "obligation", "force", "pain", "stop acting like",
        "make me happy", "prove it", "boring", "everyone else does it",
        "porn", "pictures", "video",
        # Duluth Wheel
        "forcing sex", "making you do sexual things", "criticizing sexuality",
        "withholding affection", "using jealousy sexually",
        # NDCC Ch. 12
        "sexual assault", "sexual exploitation", "non-consensual",
        # New slang
        "thirst trap", "nudes", "sext", "slide into DMs", "catfish"
        # Expanded
        "pressured for sex", "forced to watch porn", "forced to perform acts", "withholding intimacy",
        "threaten to cheat", "threaten to leave if no sex", "forced pregnancy", "birth control sabotage",
        "stealthing", "unwanted touching", "sexual blackmail", "revenge porn"
    ],
    "Digital / Tech Abuse": [
        "share location", "read texts", "check emails", "social media password",
        "who liked your photo", "delete that post", "spyware", "camera",
        "recording", "listening", "tracker", "airtag", "find my iphone",
        "history", "browser history", "fake profile",
        # Duluth Wheel
        "monitoring online activity", "hacking accounts", "cyberstalking",
        "revenge porn", "impersonation", "posting without consent",
        # NDCC Ch. 12
        "electronic harassment", "digital impersonation", "online threats",
        # New slang
        "finsta", "ghost account", "subtweet", "slide into DMs", "blockchain scam"
        # Expanded
        "forced to share passwords", "demanding access to phone", "installing tracking apps",
        "posting without consent", "threatening to leak nudes", "catfishing", "impersonating online",
        "spamming calls", "spamming messages", "public shaming online", "doxxing", "cyberbullying"
    ]
}
