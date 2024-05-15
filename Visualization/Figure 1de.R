#load packages
require(vegan)
require(ape)
require(ggplot2)
require(ggrepel)




varespec <- read.delim('genus.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE)

varechem <- read.delim('FACTORS.txt', row.names = 1, sep = '\t', stringsAsFactors = FALSE, check.names = FALSE)

group <- read.delim('group_pcoa_factor.txt', sep = '\t', stringsAsFactors = FALSE)

distance <- vegdist(varespec, method = 'bray') 
pcoa <- pcoa(vegdist(varespec))

pcoa_eig <- (pcoa$values$Relative_eig)[1:2] / sum(pcoa$values$Relative_eig)

#Vector fitting with PCoA
pcoa.envt.fit <- envfit(pcoa$vectors[,1:2] ~  scale(tos) + scale(sos) +scale(spco2) + scale(mlotst) + scale(o2os) + scale(po4os)+ scale(sios)+ scale(dfeos)+ scale(co3)+ scale(no3os),data = varechem,  permutations = 999,na.rm = TRUE)


##########################################################################################
##################################Make visualizations#####################################
##########################################################################################

#Start with the PCoA results since this is most translatable to subsequent analyses

#Organic horizon
pcoa.plot <- data.frame(pcoa$vectors[,1:2])
pcoa.plot$names <- rownames(pcoa.plot)
names(pcoa.plot)[1:2] <- c('PCoA1', 'PCoA2')

pcoa.plot <- merge(pcoa.plot, group,by ='names', all.x = TRUE)

pcoa.envt.fit.results <- data.frame(scores(pcoa.envt.fit, c("vectors")))
pcoa.envt.fit.results$p.value <- pcoa.envt.fit$vectors$pvals                                      
pcoa.envt.fit.results$r.value <- pcoa.envt.fit$vectors$r                                      
pcoa.envt.fit.results$labels <- c("tos", "sos", "spco2", "mlotst",
                                      "o2os", "po4os", "SIO4", "dfeos", "co3", "no3os")
pcoa.envt.fit.results$significance <- ifelse(pcoa.envt.fit.results$p.value < 0.05, "solid", "dashed")
pcoa.envt.fit.results$sig2 <- pcoa.envt.fit.results$significance
pcoa.envt.fit.results$sig2 <- gsub("dashed", "NS", pcoa.envt.fit.results$sig2)
pcoa.envt.fit.results$sig2 <- gsub("solid", "Sig.", pcoa.envt.fit.results$sig2)

plot <- ggplot(pcoa.plot, aes(x = PCoA1, y = PCoA2)) +
  theme(panel.grid = element_blank(), panel.background = element_rect(color = 'black', fill = 'transparent'), legend.key = element_rect(fill = 'transparent')) +
  geom_vline(xintercept = 0, color = 'gray', size = 0.3) + 
  geom_hline(yintercept = 0, color = 'gray', size = 0.3) +
  geom_point(aes(color =ProvCode,shape=time), size = 2, alpha = 0.8) + 
  scale_shape_manual(values = c(15,16,17,18,11,12,13)) + 
  labs(x = paste('PCo1 (', round(100 * pcoa_eig[1], 2), '%)'), y = paste('PCo2 (', round(100 * pcoa_eig[2], 2), '%)'))+
  annotate("segment", x = rep(0, length(pcoa.envt.fit.results$Axis.1)), 
           xend = 0.45*pcoa.envt.fit.results$Axis.1, 
           y = rep(0, length(pcoa.envt.fit.results$Axis.1)), 
           yend = 0.45*pcoa.envt.fit.results$Axis.2, 
           linetype = pcoa.envt.fit.results$significance,
           colour = "black", size=0.5, arrow=arrow(length = unit(.2,"cm"))) +
  geom_text_repel(data = pcoa.envt.fit.results, aes(x = 0.5*Axis.1, 
                                                        y = 0.5*Axis.2, 
                                                        label = labels),
                  colour = "black")

plot

adonis_result <- adonis(varespec~time, group, permutations = 999, distance = 'bray')

adonis_result$aov.tab$'Pr(>F)'
adonis_result$aov.tab$R2

