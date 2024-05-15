library(ggplot2)

# setup folder path containing change-information for each microbial index
folder_path <- "Figure3ef"

# obtain all files
file_list <- list.files(path = folder_path, pattern = "\\.csv$", full.names = TRUE)

# visualization for each microbial index
for (file_name in file_list) {
  df <- read.csv(file_name)
  
  df_long <- pivot_longer(df, cols = -Change, names_to = "SSP", values_to = "Count")
  
  p <- ggplot(df_long, aes(x = SSP, y = Count, fill = Change)) +
    geom_bar(stat = "identity", position = "identity") +
    geom_hline(yintercept = 0, color = "black", size = 0.05) +
    scale_fill_manual(values = c("increase" = "red", "decrease" = "blue"))+
    theme_void() + 
    theme(aspect.ratio = 1, 
          panel.border = element_rect(colour = "black", fill = NA, size = 0.2), 
          legend.position = "none")
  
  # save pdf
  output_file <- paste0(folder_path, "/output/", tools::file_path_sans_ext(basename(file_name)), ".pdf")
  ggsave(output_file, plot = p, device = "pdf", width = 1, height = 1)
}

print("All files processed and plots saved.")
