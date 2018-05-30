import re

desc = str('<divclass=\"content\">庄严的皇宫内，十二位以属相命名的大内密探肩负着贴身保护皇上的重任，其中高天九外号“灵灵狗”（古天乐 饰）是一位满脑子充满奇想秒招的发明家。他靠各种“法宝”在保护皇上的过程中屡建奇功，但对于自己风情万种却功艺高强的未婚妻梅希望（大S 饰）的一片痴心，“灵灵狗”的反应却表现的相当木讷。为了让这“灵灵狗”这个木瓜开窍，梅希望想出了一个试探“灵灵狗”的办法。\n深宫之类忠奸难辨，暗藏杀机。围绕公主选附马一事，各方面的力量都暗自勾结，企图谋权篡位并消灭以“灵灵狗”为首的大内密探，皇上安危遭受威胁，十二密探面临前所未有的挑战。</div><style>            body { font-family: -apple-system; }            .content {            color: #494949;            }            .content a:link,            .content a:hover,            .content a:visited,            .content a:active {            color: #42BD56;            text-decoration: none;            }            .abstract {            font-size: 13px;            line-height: 18px;            }            .detail {            font-size: 15px;            }            .abstract p {            margin-bottom: 18px;            }            .content p:last-child {            margin: 0;            }            </style>')


a = re.search('^<[\s\S]*>([\s\S]*)</div>', desc).group(1)

print(a)

