library(ggplot2)
library(reshape2)

#load data
data <- read.delim('Supplementary_Figure_7.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE,na.strings="na")
stat_data <- read.delim('Supplementary_Figure_7_stat.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE,na.strings="na")

data_long <- reshape2::melt(data, id.vars = "sample")

data_long <- merge(data_long, stat_data, by.x = "variable", by.y = "variable")


# plot
ggplot(data_long, aes(x = value, fill = variable)) + 
  geom_density(alpha = 0.75) + 
  facet_wrap(~ variable, scales = "free") + 
  #labs(x = "Value", y = "", title = "Density Distribution") +
  geom_text(data = unique(data_long[, c("variable", "cv")]), aes(label = paste("CV:", round(cv, 2),"%"), x = Inf, y = Inf), hjust = 1.2, vjust = 1.8, size = 3) + 
  theme_minimal() +
  theme(
    panel.border = element_rect(colour = "black", fill=NA, linewidth=1),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(), 
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.title.y = element_blank(), 
    strip.background = element_blank(), 
    legend.position = "none",
    strip.text.x = element_text(size=10)
  ) 


