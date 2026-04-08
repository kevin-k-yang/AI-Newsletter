from models import DailyDigest

MOCK_DIGEST = DailyDigest(
    date="2026-04-07",
    sections=[
        {
            "section": "sports",
            "summary": (
                "The NBA playoffs are heating up with several surprising upsets in the first round. "
                "The defending champions face elimination after dropping three straight games, while a "
                "young underdog team has captured the nation's attention with their Cinderella run. "
                "Meanwhile, the MLB season is in full swing with early-season surprises reshaping "
                "division races across both leagues."
            ),
            "substories": [
                {
                    "id": "sports-1",
                    "title": "Defending Champions on the Brink of Elimination",
                    "summary": (
                        "In a stunning turn of events, the defending NBA champions find themselves "
                        "down 3-1 in their first-round playoff series. Key injuries and a lack of "
                        "depth have plagued the team, while their opponents have found a new gear "
                        "behind a breakout performance from their second-year guard."
                    ),
                    "url": "https://example.com/nba-playoffs-upset",
                },
                {
                    "id": "sports-2",
                    "title": "Rookie Pitcher Throws No-Hitter in MLB Debut",
                    "summary": (
                        "A 22-year-old rookie pitcher made history by throwing a no-hitter in his "
                        "major league debut, becoming only the fifth pitcher in MLB history to "
                        "accomplish the feat."
                    ),
                    "url": "https://example.com/rookie-no-hitter",
                },
                {
                    "id": "sports-3",
                    "title": "FIFA Announces Expanded Club World Cup Format",
                    "summary": (
                        "FIFA has unveiled a new expanded format for the Club World Cup that will "
                        "feature 48 teams starting in 2028."
                    ),
                    "url": "https://example.com/fifa-club-world-cup",
                },
            ],
        },
        {
            "section": "tech",
            "summary": (
                "The tech industry is buzzing with new developments in AI regulation and a wave of "
                "product launches. A major open-source AI model release has disrupted the competitive "
                "landscape, while governments worldwide are racing to establish guardrails."
            ),
            "substories": [
                {
                    "id": "tech-1",
                    "title": "Open-Source AI Model Rivals Leading Commercial Systems",
                    "summary": (
                        "A consortium of research labs has released a new open-source large language "
                        "model that benchmarks within striking distance of the top commercial offerings."
                    ),
                    "url": "https://example.com/open-source-ai",
                },
                {
                    "id": "tech-2",
                    "title": "EU Passes Comprehensive AI Safety Framework",
                    "summary": (
                        "The European Union has passed its most detailed AI regulation to date, "
                        "establishing mandatory safety testing for high-risk AI systems."
                    ),
                    "url": "https://example.com/eu-ai-regulation",
                },
                {
                    "id": "tech-3",
                    "title": "Sub-$500 AR Glasses Hit the Consumer Market",
                    "summary": (
                        "Two major electronics manufacturers have announced AR glasses priced under "
                        "$500, a threshold that analysts consider critical for mass adoption."
                    ),
                    "url": "https://example.com/ar-glasses-affordable",
                },
            ],
        },
        {
            "section": "finance",
            "summary": (
                "Markets are responding to mixed economic signals as the Federal Reserve hints at a "
                "potential rate adjustment later this quarter. Corporate earnings season has delivered "
                "surprises on both ends, with traditional retail struggling while green energy companies "
                "post record revenues."
            ),
            "substories": [
                {
                    "id": "finance-1",
                    "title": "Federal Reserve Signals Possible Rate Cut in June",
                    "summary": (
                        "Federal Reserve officials have signaled openness to a rate cut at their "
                        "June meeting, citing cooling inflation data and a softening labor market."
                    ),
                    "url": "https://example.com/fed-rate-cut",
                },
                {
                    "id": "finance-2",
                    "title": "Green Energy Sector Posts Record Q1 Earnings",
                    "summary": (
                        "The renewable energy sector has reported its strongest first quarter ever, "
                        "with solar and wind companies seeing revenue growth exceeding 40% year-over-year."
                    ),
                    "url": "https://example.com/green-energy-earnings",
                },
                {
                    "id": "finance-3",
                    "title": "Major Bank Launches Crypto Custody Service",
                    "summary": (
                        "One of the world's largest banks has announced a full-service cryptocurrency "
                        "custody platform for institutional clients."
                    ),
                    "url": "https://example.com/bank-crypto-custody",
                },
            ],
        },
        {
            "section": "world",
            "summary": (
                "Global attention is focused on a new international climate agreement that sets more "
                "aggressive emissions targets for 2035. Meanwhile, diplomatic tensions in the South "
                "China Sea have escalated following a series of naval incidents."
            ),
            "substories": [
                {
                    "id": "world-1",
                    "title": "195 Nations Sign Landmark Climate Accord with 2035 Targets",
                    "summary": (
                        "In a historic agreement, 195 nations have committed to reducing carbon "
                        "emissions by 60% from 2005 levels by 2035."
                    ),
                    "url": "https://example.com/climate-accord-2035",
                },
                {
                    "id": "world-2",
                    "title": "South China Sea Tensions Prompt UN Emergency Session",
                    "summary": (
                        "The UN Security Council convened an emergency session after a series of "
                        "naval confrontations in the South China Sea raised fears of wider conflict."
                    ),
                    "url": "https://example.com/south-china-sea-tensions",
                },
                {
                    "id": "world-3",
                    "title": "Drought-Resistant Crops Transform East African Agriculture",
                    "summary": (
                        "A new generation of drought-resistant crop varieties developed through "
                        "advanced gene editing is being deployed across Kenya, Ethiopia, and Tanzania."
                    ),
                    "url": "https://example.com/drought-resistant-crops",
                },
            ],
        },
    ],
)
