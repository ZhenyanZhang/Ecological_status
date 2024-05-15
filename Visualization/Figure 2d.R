# Libraries
library(tidyverse)
library(hrbrthemes)
library(viridisLite)
library(viridis)
library(ggplot2)
library(dplyr)
library(tidyr)


# road data
data <- read.delim('Figure 2d.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE,na.strings="na")


# Plot
ggplot(data, aes(x=ES, y=shannon,color=ES)) +
   geom_boxplot(notch=F,notchwidth=0.5,width =0.3,outlier.shape = NA) +
   theme(panel.grid = element_blank(), panel.background = element_rect(color = 'black', fill = 'transparent'), legend.key = element_rect(fill = 'transparent'))+
   xlab("")

