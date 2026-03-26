import glob

for filename in glob.glob('../../../*.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # very specific replacements
        content = content.replace('孙女"女红"首制', '孙女“女红”首制')
        content = content.replace('称为"女红"', '称为“女红”')
        content = content.replace('有"绣万国于一锦"之说', '有“绣万国于一锦”之说')
        content = content.replace('谓之"针绝"', '谓之“针绝”')
        content = content.replace('叙述，"宋人之绣', '叙述，“宋人之绣')
        content = content.replace('光彩射目。"', '光彩射目。”')
        content = content.replace('成了"家家养蚕，户户刺绣"的盛况', '成了“家家养蚕，户户刺绣”的盛况')
        content = content.replace('称为"绣市"', '称为“绣市”')
        content = content.replace('创"仿真绣"', '创“仿真绣”')
        content = content.replace('创"乱针绣"', '创“乱针绣”')
        content = content.replace('讲究"平、齐、细、密、和、光、顺、匀"的特点', '讲究“平、齐、细、密、和、光、顺、匀”的特点')
        content = content.replace('形成"平、齐、细、密、匀、顺、和、光"的特点', '形成“平、齐、细、密、匀、顺、和、光”的特点')
        content = content.replace('又称"双面绣"', '又称“双面绣”')

        # 紫砂.json fixes
        content = content.replace('称为"供春壶"', '称为“供春壶”')
        content = content.replace('俗称"曼生壶"', '俗称“曼生壶”')
        content = content.replace('讲究"方非一式，圆不一相"', '讲究“方非一式，圆不一相”')
        content = content.replace('一种是"泥片打身筒"', '一种是“泥片打身筒”')
        content = content.replace('另一种是"镶身筒"', '另一种是“镶身筒”')
        content = content.replace('称为"明针"', '称为“明针”')

        # 剪纸.json fixes
        content = content.replace('要求"千刻不落，万剪不断"', '要求“千刻不落，万剪不断”')
        content = content.replace('分为"阴刻"', '分为“阴刻”')
        content = content.replace('和"阳刻"', '和“阳刻”')
        
        # 蜡染.json fixes
        content = content.replace('产生"冰纹"', '产生“冰纹”')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        pass
