CREATE TABLE IF NOT EXISTS main (
    UserID INTEGER DEFAULT 0,
    Messages INTEGER DEFAULT 0,

    Diamond INTEGER DEFAULT 0,
    Platinum INTEGER DEFAULT 0,
    Gold INTEGER DEFAULT 0,
    Silver INTEGER DEFAULT 0,
    Bronze INTEGER DEFAULT 0,

    TotalSP FLOAT DEFAULT 0,
    LaughPts INTEGER DEFAULT 0,
    XPts INTEGER DEFAULT 0,
    RecPts INTEGER DEFAULT 0,
    Coins INTEGER DEFAULT 0,
    MonthlySP FLOAT DEFAULT 0,
    SPBonus INTEGER DEFAULT 0,
    SPBonusTime INTEGER DEFAULT 0,

    GeneralLevel INTEGER DEFAULT 1,
    GeneralXP INTEGER DEFAULT 0,
    GenLevelLimit INTEGER DEFAULT 100,
    GenLevelRest INTEGER DEFAULT 0,
    LigtasPoints INTEGER DEFAULT 0,
    LPCooldown INTEGER DEFAULT 0,
    LevelUpType INTEGER DEFAULT 0,

    BannerChoice INTEGER DEFAULT 0,
    TextBG TEXT DEFAULT "#FFFFFF",
    PolyBG TEXT DEFAULT "#FFFFFF",
    OutlineBG TEXT DEFAULT "#000000",

    MessageIDS TEXT DEFAULT "{}";
    PRIMARY KEY(UserID)
);

CREATE TABLE IF NOT EXISTS global (
    Maintenance INTEGER DEFAULT 0,
    MaintenanceDuration INTEGER DEFAULT 0,
    MMA INTEGER DEFAULT 0,
);

-- Create the themes table
CREATE TABLE IF NOT EXISTS themes (
    Banner1 INT DEFAULT 0,
    Banner2 INT DEFAULT 0,
    Banner3 INT DEFAULT 0,
    Banner4 INT DEFAULT 0,
    Banner5 INT DEFAULT 0,
    Banner6 INT DEFAULT 0,
    Banner7 INT DEFAULT 0,
    Banner8 INT DEFAULT 0,
    Banner9 INT DEFAULT 0,
    Banner10 INT DEFAULT 0,
    Banner11 INT DEFAULT 0,
    Banner12 INT DEFAULT 0,
    Banner13 INT DEFAULT 0,
    Banner14 INT DEFAULT 0,
    Banner15 INT DEFAULT 0,
    Banner16 INT DEFAULT 0,
    Banner17 INT DEFAULT 0,
    Banner18 INT DEFAULT 0,
    Banner19 INT DEFAULT 0,
    Banner20 INT DEFAULT 0,
    Banner21 INT DEFAULT 0,
    Banner22 INT DEFAULT 0,
    Banner23 INT DEFAULT 0,
    Banner24 INT DEFAULT 0,
    Banner25 INT DEFAULT 0,
    Banner26 INT DEFAULT 0,
    Banner27 INT DEFAULT 0,
    Banner28 INT DEFAULT 0,
    Banner29 INT DEFAULT 0,
    Banner30 INT DEFAULT 0
);

-- Create the colors table
CREATE TABLE IF NOT EXISTS colors (
    TextColor1 INT DEFAULT 0,
    TextColor2 INT DEFAULT 0,
    TextColor3 INT DEFAULT 0,
    TextColor4 INT DEFAULT 0,
    TextColor5 INT DEFAULT 0,
    TextColor6 INT DEFAULT 0,
    TextColor7 INT DEFAULT 0,
    TextColor8 INT DEFAULT 0,
    TextColor9 INT DEFAULT 0,
    TextColor10 INT DEFAULT 0,
    TextColor11 INT DEFAULT 0,
    TextColor12 INT DEFAULT 0,
    TextColor13 INT DEFAULT 0,
    TextColor14 INT DEFAULT 0,
    TextColor15 INT DEFAULT 0,
    TextColor16 INT DEFAULT 0,
    TextColor17 INT DEFAULT 0,
    TextColor18 INT DEFAULT 0,
    TextColor19 INT DEFAULT 0,
    TextColor20 INT DEFAULT 0,
    TextColor21 INT DEFAULT 0,
    TextColor22 INT DEFAULT 0,
    TextColor23 INT DEFAULT 0,
    TextColor24 INT DEFAULT 0,
    TextColor25 INT DEFAULT 0,
    TextColor26 INT DEFAULT 0,
    TextColor27 INT DEFAULT 0,
    TextColor28 INT DEFAULT 0,
    TextColor29 INT DEFAULT 0,
    TextColor30 INT DEFAULT 0,
    OutlineColor1 INT DEFAULT 0,
    OutlineColor2 INT DEFAULT 0,
    OutlineColor3 INT DEFAULT 0,
    OutlineColor4 INT DEFAULT 0,
    OutlineColor5 INT DEFAULT 0,
    OutlineColor6 INT DEFAULT 0,
    OutlineColor7 INT DEFAULT 0,
    OutlineColor8 INT DEFAULT 0,
    OutlineColor9 INT DEFAULT 0,
    OutlineColor10 INT DEFAULT 0,
    OutlineColor11 INT DEFAULT 0,
    OutlineColor12 INT DEFAULT 0,
    OutlineColor13 INT DEFAULT 0,
    OutlineColor14 INT DEFAULT 0,
    OutlineColor15 INT DEFAULT 0,
    OutlineColor16 INT DEFAULT 0,
    OutlineColor17 INT DEFAULT 0,
    OutlineColor18 INT DEFAULT 0,
    OutlineColor19 INT DEFAULT 0,
    OutlineColor20 INT DEFAULT 0,
    OutlineColor21 INT DEFAULT 0,
    OutlineColor22 INT DEFAULT 0,
    OutlineColor23 INT DEFAULT 0,
    OutlineColor24 INT DEFAULT 0,
    OutlineColor25 INT DEFAULT 0,
    OutlineColor26 INT DEFAULT 0,
    OutlineColor27 INT DEFAULT 0,
    OutlineColor28 INT DEFAULT 0,
    OutlineColor29 INT DEFAULT 0,
    OutlineColor30 INT DEFAULT 0
);