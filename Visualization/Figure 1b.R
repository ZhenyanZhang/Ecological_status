library(ggplot2)

#导入数据
data <- read.delim('Figure1b.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE,na.strings="na")

ggplot(data, aes(x=value, y=value)) + 
  geom_point(aes(color =sample), size = 1,shape=16, alpha = 0.8)+
  scale_color_manual(values = c('red', 'lightgrey')) +
  theme(panel.grid = element_blank(), panel.background = element_rect(color = 'black', fill = 'transparent'), legend.key = element_rect(fill = 'transparent'))
