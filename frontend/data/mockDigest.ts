import { DailyDigest } from "../types";

export const mockDigest: DailyDigest = {
  date: "2026-04-07",
  sections: [
    {
      section: "sports",
      summary:
        "The NBA playoffs are heating up with several surprising upsets in the first round. The defending champions face elimination after dropping three straight games, while a young underdog team has captured the nation's attention with their Cinderella run. Meanwhile, the MLB season is in full swing with early-season surprises reshaping division races across both leagues.",
      substories: [
        {
          id: "sports-1",
          title: "Defending Champions on the Brink of Elimination",
          summary:
            "In a stunning turn of events, the defending NBA champions find themselves down 3-1 in their first-round playoff series. Key injuries and a lack of depth have plagued the team, while their opponents have found a new gear behind a breakout performance from their second-year guard who is averaging 28 points in the series.",
          url: "https://example.com/nba-playoffs-upset",
        },
        {
          id: "sports-2",
          title: "Rookie Pitcher Throws No-Hitter in MLB Debut",
          summary:
            "A 22-year-old rookie pitcher made history by throwing a no-hitter in his major league debut, becoming only the fifth pitcher in MLB history to accomplish the feat. The left-hander struck out 11 batters and walked just two in a dominant performance that has scouts and analysts re-evaluating their preseason projections.",
          url: "https://example.com/rookie-no-hitter",
        },
        {
          id: "sports-3",
          title: "FIFA Announces Expanded Club World Cup Format",
          summary:
            "FIFA has unveiled a new expanded format for the Club World Cup that will feature 48 teams starting in 2028. The decision has drawn mixed reactions from clubs, players' unions, and fans, with concerns about an already crowded calendar conflicting with excitement about more global matchups between top clubs from different continents.",
          url: "https://example.com/fifa-club-world-cup",
        },
      ],
    },
    {
      section: "tech",
      summary:
        "The tech industry is buzzing with new developments in AI regulation and a wave of product launches. A major open-source AI model release has disrupted the competitive landscape, while governments worldwide are racing to establish guardrails. On the consumer side, a new generation of AR glasses is finally reaching mainstream price points, sparking renewed interest in spatial computing.",
      substories: [
        {
          id: "tech-1",
          title: "Open-Source AI Model Rivals Leading Commercial Systems",
          summary:
            "A consortium of research labs has released a new open-source large language model that benchmarks within striking distance of the top commercial offerings. The model, which can run on consumer hardware, has sparked a wave of innovation among independent developers and raised questions about the sustainability of closed-model business strategies.",
          url: "https://example.com/open-source-ai",
        },
        {
          id: "tech-2",
          title: "EU Passes Comprehensive AI Safety Framework",
          summary:
            "The European Union has passed its most detailed AI regulation to date, establishing mandatory safety testing for high-risk AI systems and requiring transparency reports from companies deploying AI at scale. Tech companies have six months to comply, and early reactions suggest the rules could become a de facto global standard similar to GDPR.",
          url: "https://example.com/eu-ai-regulation",
        },
        {
          id: "tech-3",
          title: "Sub-$500 AR Glasses Hit the Consumer Market",
          summary:
            "Two major electronics manufacturers have announced AR glasses priced under $500, a threshold that analysts consider critical for mass adoption. The devices feature all-day battery life and seamless integration with existing smartphone ecosystems, marking a significant shift from the bulky, expensive headsets that have dominated the market.",
          url: "https://example.com/ar-glasses-affordable",
        },
      ],
    },
    {
      section: "finance",
      summary:
        "Markets are responding to mixed economic signals as the Federal Reserve hints at a potential rate adjustment later this quarter. Corporate earnings season has delivered surprises on both ends, with traditional retail struggling while green energy companies post record revenues. Cryptocurrency markets have stabilized after last month's volatility, with institutional adoption continuing to grow steadily.",
      substories: [
        {
          id: "finance-1",
          title: "Federal Reserve Signals Possible Rate Cut in June",
          summary:
            "Federal Reserve officials have signaled openness to a rate cut at their June meeting, citing cooling inflation data and a softening labor market. The announcement sent bond yields lower and boosted equity markets, with rate-sensitive sectors like real estate and utilities leading the gains. Economists remain divided on whether the cut would be premature.",
          url: "https://example.com/fed-rate-cut",
        },
        {
          id: "finance-2",
          title: "Green Energy Sector Posts Record Q1 Earnings",
          summary:
            "The renewable energy sector has reported its strongest first quarter ever, with solar and wind companies seeing revenue growth exceeding 40% year-over-year. Analysts attribute the surge to a combination of government incentives, falling production costs, and increasing corporate demand for clean energy procurement agreements.",
          url: "https://example.com/green-energy-earnings",
        },
        {
          id: "finance-3",
          title: "Major Bank Launches Crypto Custody Service",
          summary:
            "One of the world's largest banks has announced a full-service cryptocurrency custody platform for institutional clients, marking a significant milestone in mainstream financial adoption of digital assets. The service will initially support Bitcoin and Ethereum, with plans to expand to additional tokens pending regulatory approval.",
          url: "https://example.com/bank-crypto-custody",
        },
      ],
    },
    {
      section: "world",
      summary:
        "Global attention is focused on a new international climate agreement that sets more aggressive emissions targets for 2035. Meanwhile, diplomatic tensions in the South China Sea have escalated following a series of naval incidents, prompting emergency UN Security Council sessions. In humanitarian news, a breakthrough in drought-resistant crop technology is being deployed across East Africa, offering hope for food security in the region.",
      substories: [
        {
          id: "world-1",
          title: "195 Nations Sign Landmark Climate Accord with 2035 Targets",
          summary:
            "In a historic agreement, 195 nations have committed to reducing carbon emissions by 60% from 2005 levels by 2035, the most ambitious target ever set in an international climate framework. The accord includes a $500 billion annual fund to support developing nations' transitions and introduces binding enforcement mechanisms for the first time.",
          url: "https://example.com/climate-accord-2035",
        },
        {
          id: "world-2",
          title: "South China Sea Tensions Prompt UN Emergency Session",
          summary:
            "The UN Security Council convened an emergency session after a series of naval confrontations in the South China Sea raised fears of wider conflict. Multiple nations have reported close encounters between military vessels, and diplomatic channels are being strained as competing territorial claims intensify. International mediators are calling for immediate de-escalation.",
          url: "https://example.com/south-china-sea-tensions",
        },
        {
          id: "world-3",
          title: "Drought-Resistant Crops Transform East African Agriculture",
          summary:
            "A new generation of drought-resistant crop varieties developed through advanced gene editing is being deployed across Kenya, Ethiopia, and Tanzania. Early results show yield improvements of up to 70% compared to traditional varieties under drought conditions, potentially transforming food security for millions of people in the region.",
          url: "https://example.com/drought-resistant-crops",
        },
      ],
    },
  ],
};
