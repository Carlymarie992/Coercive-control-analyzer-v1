"""
DARVO (Deny, Attack, and Reverse Victim and Offender) Tactics Indicators.

This module contains patterns and keywords for identifying DARVO manipulation
tactics commonly used by abusers, particularly in legal and institutional contexts.
"""

# DARVO Pattern Indicators
DARVO_INDICATORS = {
    "Deny": {
        "minimization": [
            "it wasn't that bad", "you're exaggerating", "it's not a big deal",
            "you're making it worse than it was", "that never happened",
            "you're remembering it wrong", "it wasn't like that", "you're blowing it out of proportion",
            "I barely", "I hardly", "all I did was", "I only", "just a little",
            "not as bad as", "everyone does it", "it's normal", "that's just how I am"
        ],
        "outright_denial": [
            "I never said that", "I never did that", "that didn't happen",
            "you're lying", "you made that up", "prove it", "where's your evidence",
            "that's not true", "I would never", "you're making things up",
            "I don't remember that", "you're confused", "you're mistaken",
            "that's fabricated", "complete lies", "false accusations"
        ],
        "blame_shifting": [
            "you made me", "you provoked me", "you started it",
            "if you hadn't", "you caused this", "it's your fault",
            "you pushed me to", "you left me no choice", "what did you expect",
            "you should have", "you shouldn't have", "because of you",
            "you're responsible for", "you brought this on yourself"
        ]
    },
    
    "Attack": {
        "credibility_attacks": [
            "you're crazy", "you're mentally ill", "you're unstable",
            "you need help", "you're delusional", "you're paranoid",
            "you're irrational", "you can't be trusted", "you're unreliable",
            "everyone knows you're", "history of lying", "track record",
            "you always lie", "nobody believes you", "you're not credible",
            "you have issues", "seek therapy", "get help"
        ],
        "character_assassination": [
            "you're a bad mother", "you're a bad father", "unfit parent",
            "bad person", "terrible", "vindictive", "vengeful",
            "manipulative", "controlling", "abusive", "toxic",
            "you're the problem", "you're the one", "you're actually",
            "you're just like", "narcissist", "sociopath", "psycho"
        ],
        "threat_of_consequences": [
            "I'll tell everyone", "I'll expose you", "everyone will know",
            "you'll lose the kids", "I'll take the children", "custody",
            "I'll ruin you", "destroy your reputation", "nobody will believe you",
            "you'll regret this", "you'll pay for this", "I'll make sure",
            "the court will see", "the judge will know", "I'll prove",
            "evidence against you", "document everything", "legal action"
        ],
        "gaslighting": [
            "that never happened", "you're imagining things", "you're too sensitive",
            "you're overreacting", "you can't take a joke", "you're being dramatic",
            "you're twisting things", "that's not what I meant", "you misunderstood",
            "you're reading too much into it", "you're being ridiculous",
            "you're making a scene", "calm down", "relax"
        ]
    },
    
    "Reverse_Victim_Offender": {
        "self_victimization": [
            "I'm the victim here", "I'm the one suffering", "what about me",
            "I'm being attacked", "I'm being abused", "I'm being harassed",
            "you're hurting me", "you're destroying me", "I can't take this anymore",
            "look what you've done to me", "I'm the one in pain",
            "I'm being treated unfairly", "I'm being persecuted",
            "this is abuse", "you're abusing me", "I need protection from you"
        ],
        "victim_blaming": [
            "you're the real abuser", "you're the manipulator", "you're controlling",
            "you're the violent one", "you started this", "you're the aggressor",
            "you're alienating the children", "parental alienation",
            "you're turning them against me", "you're poisoning them",
            "you're using the children", "you're the narcissist",
            "you're projecting", "you're doing exactly what you accuse me of"
        ],
        "false_equivalence": [
            "we're both", "you do it too", "you're just as bad",
            "you're no better", "we both", "mutual abuse",
            "it's mutual", "both sides", "we're equally",
            "you also", "what about when you", "remember when you",
            "you've done worse", "at least I didn't"
        ],
        "protective_parent_reversal": [
            "I'm protecting the children from you", "the children are afraid of you",
            "I'm the safe parent", "you're unstable around the kids",
            "I'm the primary caregiver", "the children need me",
            "you're a danger to them", "I'm keeping them safe",
            "they don't want to see you", "they're scared of you",
            "I'm acting in their best interest"
        ]
    },
    
    # Institutional/Legal DARVO patterns
    "Institutional_DARVO": {
        "court_manipulation": [
            "false allegations", "she's lying to the court", "he's deceiving the judge",
            "fabricated evidence", "coached the children", "parental alienation syndrome",
            "high conflict parent", "making false reports", "weaponizing the system",
            "abusing the legal process", "frivolous complaints",
            "attention seeking", "playing the victim card"
        ],
        "professional_credibility": [
            "I'm a professional", "I'm a respected member", "my reputation",
            "my standing in the community", "never had complaints before",
            "exemplary record", "decorated", "award winning",
            "everyone knows me as", "ask anyone", "references will show"
        ],
        "systemic_bias_indicators": [
            "mothers always get", "fathers are discriminated against",
            "the system is biased", "family court favors", "automatically believes",
            "without investigation", "rushed to judgment", "presumed guilty",
            "not given a fair chance", "predetermined outcome"
        ]
    }
}

# Compound patterns that indicate DARVO tactics when appearing together
DARVO_COMPOUND_PATTERNS = {
    "deny_then_attack": {
        "description": "Denying wrongdoing immediately followed by attacking the accuser",
        "pattern": ["deny", "attack"],
        "window_messages": 3
    },
    "attack_then_reverse": {
        "description": "Attacking credibility then claiming to be the victim",
        "pattern": ["attack", "reverse"],
        "window_messages": 5
    },
    "full_darvo_sequence": {
        "description": "Complete DARVO sequence: deny, attack, then reverse",
        "pattern": ["deny", "attack", "reverse"],
        "window_messages": 10
    }
}

# Severity scoring weights
DARVO_SEVERITY_WEIGHTS = {
    "Deny": {
        "minimization": 1,
        "outright_denial": 2,
        "blame_shifting": 3
    },
    "Attack": {
        "credibility_attacks": 3,
        "character_assassination": 4,
        "threat_of_consequences": 5,
        "gaslighting": 3
    },
    "Reverse_Victim_Offender": {
        "self_victimization": 3,
        "victim_blaming": 4,
        "false_equivalence": 2,
        "protective_parent_reversal": 5
    },
    "Institutional_DARVO": {
        "court_manipulation": 5,
        "professional_credibility": 2,
        "systemic_bias_indicators": 3
    }
}

# Child-specific DARVO patterns (high priority)
CHILD_FOCUSED_DARVO = {
    "child_weaponization": [
        "the children say", "ask the kids", "children don't lie",
        "they told me about", "they witnessed", "they're afraid of you",
        "they don't want to see you", "they asked me to",
        "protecting the children", "for the kids' safety"
    ],
    "parental_alienation_claims": [
        "parental alienation", "turning the children against me",
        "poisoning their minds", "coaching the children",
        "brainwashing", "manipulating the kids"
    ],
    "custody_threats": [
        "you'll never see them again", "I'll get full custody",
        "no visitation", "supervised visits only", "unfit parent",
        "not safe around children", "danger to the kids"
    ]
}
