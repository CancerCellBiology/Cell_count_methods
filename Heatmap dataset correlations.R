library(ComplexHeatmap)
library(openxlsx)
library(circlize)
rdata<-read.xlsx('DepMap AUC correlations R.xlsx')
mat= as.matrix(rdata[,-1])
class(mat)<-"numeric"
rownames(mat) <- rdata[,1]
colnames(mat) <- c('PRISM vs\nCTRP2', 'PRISM vs\nGDSC1/2', 'CTRP2 vs\nGDSC1/2')
col_heat = colorRamp2(c(0.65, 0), c('#ff6000','white'))

pdata<-read.xlsx('DepMap AUC correlations pval.xlsx')
pmat= as.matrix(pdata[,-1])
pmat[pmat<0.001] <- 0.001
pmat[pmat>0.05] <- 0.05
class(pmat)<-"numeric"
rownames(pmat) <- pdata[,1]
colnames(pmat) <- c('PRISM vs\nCTRP2', 'PRISM vs\nGDSC1/2', 'CTRP2 vs\nGDSC1/2')

ht<-Heatmap(mat,name = "Spearman's\ncorrelation", col=col_heat, rect_gp = gpar(type = "none"),
        clustering_distance_rows = 'euclidean',  clustering_method_rows = 'ward.D2', cluster_columns = FALSE,
        show_row_names = TRUE, show_column_names = TRUE, column_names_side = "top", column_names_rot=90, column_names_centered = TRUE,
        cell_fun = function(j, i, x, y, width, height, fill) {
          if(pmat[i, j]<0.05){
          grid.circle(x = x, y = y, r = -log(pmat[i, j],2)/120, 
                      gp = gpar(fill = col_heat(mat[i, j]), col = 'black'))}
          else{
            grid.circle(x = x, y = y, r = -log(pmat[i, j],2)/120, 
                        gp = gpar(fill =  '#5b8c99', col = 'black'))
          }
          grid.text(sprintf("%.2f", mat[i, j]), x, y, gp = gpar(fontsize = 10))},
        column_dend_height = unit(1, "cm"), row_names_side = "left", width = unit(5, "cm"), height = unit(15, "cm"))


png(file='DepMap AUC correlations.png', width=10,height=10,units="in", res=1200)
draw(ht)
dev.off()

