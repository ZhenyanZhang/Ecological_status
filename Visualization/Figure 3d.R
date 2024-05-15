library(ggplot2)

# load data
data <- read.table("SSP585_changed.txt", header = TRUE, sep = "\t")

unique_values <- unique(c(data$current, data$ssp585))
positions <- setNames(seq_along(unique_values), unique_values)

data$position_current <- positions[data$current]
data$position_ssp585 <- positions[data$ssp585]

# plot
p <- ggplot(data, aes(x = factor(1), y = position_current)) +
  geom_point() +  
  geom_text(aes(label = current), vjust = -0.5) + 
  geom_point(aes(x = factor(2), y = position_ssp585)) +
  geom_text(aes(x = factor(2), y = position_ssp585, label = ssp585), vjust = -0.5) +
  geom_segment(aes(xend = factor(2), yend = position_ssp585, size = PRPPORTION), 
               lineend = 'round') +
  scale_size(range = c(0.05, 1)) + 
  labs(title = "Connections between Current and SSP119 with Proportional Line Widths",
       x = NULL, y = NULL, size = "PRPPORTION") +
  theme_minimal() +
  theme(axis.text.x = element_blank(), 
        axis.ticks.x = element_blank(), 
        axis.title.y = element_blank(),
        legend.position = "none")
print(p)

