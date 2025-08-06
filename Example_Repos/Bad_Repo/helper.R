#===============================================================================
# LIBRARIES
#===============================================================================
for(pack in c("MBESS", "lme4", "lmerTest", "RVAideMemoire", "psych", "cocor", "beepr", "kableExtra", "knitr", "psych", "cocor", "ppcor",
              "MASS", "qgraph", "Matrix", "bootnet", "reshape2", "apaTables", "Hmisc", "tidyr", "apaTables", "sjPlot", "rempsyc", "pwr")) {
    if(!(pack %in% installed.packages()[,1])) {
        install.packages(pack)  
    }
    library(pack, character.only = T)
}


#===============================================================================
# HELPER FUNCTIONS
#===============================================================================
# formating p-values
round_p <- function(x, asterisks = F) {
    if(x < .001) return(ifelse(asterisks, "***", "p < .001")) 
    if(asterisks) {
      if(x < .01) {
        return("**")
      } else {
        if(x < .05) {
          return("*")
          } else {
            return("")
          }
        }
      }
    if(round(x, 2) == 1) return("p = 1")
    p <- sprintf("%.3f", x)
    return(paste("p = ", substr(p, 2, nchar(p)), sep = ""))
}


# function for displaying results of regression models
results <- function(model, effect, family = "binomial", rounding = 2) {
    r <- function(x) sprintf(paste0("%.", rounding, "f"), x)
    coefs <- summary(model)$coefficients
    if(family == "ordinal") {
        effect <- effect + length(model$y.levels) - 1
    }
    if(family == "binomial" | family == "ordinal") {
        z <- coefs[effect, "z value"]
        p <- coefs[effect, "Pr(>|z|)"]
        e.name <- "OR"
        par <- "z"
    } else {
        z <- coefs[effect, "t value"]
        p <- coefs[effect, "Pr(>|t|)"]        
        e.name <- "b"
        if("lm" %in% class(model)) {
            df <- sprintf("%i", model$df)
        } else {
            df <- sprintf("%.1f", coefs[effect, "df"])
        }
        par <- paste0("t(", df, ")")
    }
    if("lm" %in% class(model) | family == "ordinal") {
        ES <- model$coefficients[effect]
        if(family == "ordinal") {
            CI <- confint(model)[effect - length(model$y.levels) + 1,]        
        } else {
            CI <- confint(model)[effect,]        
        }
    } else {
        ES <- fixef(model)[effect]
        CI <- confint.merMod(model, method = "Wald", parm = "beta_")[effect,] 
    }
    if(family == "binomial" | family == "ordinal") {
        ES <- exp(ES)
        CI <- exp(CI)
    }
    cat(par, " = ", sprintf("%.2f", z), ", ", 
        round_p(p), ", ",
        e.name, " = ", r(ES), ", ",
        "95% CI [", r(CI[1]), ", ",
        r(CI[2]), "]",
        sep = "")
}


# function for reporting correlations
p.cor <- function(x, y, method = "pearson", sparse = F, use = "pairwise.complete.obs") {
    shorten <- function(x) {
        s <- sprintf("%.2f", x)
        if(x >= 0) {
            return(substr(s, 2, nchar(s)))
        } else {
            return(paste0("-", substr(s, 3, nchar(s))))
        }
    }
    
    if(method == "pearson") {
        ct <- cor.test(x, y, use = use)
        if(sparse) {
          out <- sprintf("%s%s", shorten(ct$estimate), round_p(ct$p.value, asterisks = T))
        } else {
          out <- sprintf("r(%i) = %s, 95%% CI [%s, %s], %s",
                         ct$parameter, shorten(ct$estimate), shorten(ct$conf.int[1]),
                         shorten(ct$conf.int[2]), round_p(ct$p.value))
        }
    } else {
        if(method == "spearman") {
            suppressWarnings(p <- cor.test(x, y, method = "spearman", use = use)$p.value)
            sci <- spearman.ci(x, y, nrep = 1000)
            if(sparse) {
              out <- sprintf("%s%s", shorten(sci$estimate), round_p(p, asterisks = T))    
            } else {
              out <- sprintf("rS = %s, 95%% CI [%s, %s], %s",
                             shorten(sci$estimate), shorten(sci$conf.int[1]),
                             shorten(sci$conf.int[2]), round_p(p))    
            }
        } else {
            out <- "method must be either 'spearman' or 'pearson'!"
        }
    }
    out
}


# McCall transformation
mccall <- function(x) qnorm((rank(x, ties.method = "average") - 0.5) / length(x))


# function for reporting t-tests
pt.test <- function(x, y = NULL, paired = FALSE, means = F, round = 2, mu = 0, as.char = F, sparse = F) { 
  if(is.null(y)) {
    t <- t.test(x, mu = mu)
  } else {
    t <- t.test(x, y, paired = paired, var.equal = T, mu = mu)
  }
  
  capture.output(
    if(paired | is.null(y)) {
      cis <- ci.sm(ncp = t$statistic, N = t$parameter + 1)
    } else {
      cis <- ci.smd(ncp = t$statistic, n.1 = length(x), n.2 = length(y))
    }
  )
  if(sparse) {
    out <- sprintf("%.2f%s", ifelse(paired | is.null(y), cis$Standardized, cis$smd), round_p(t$p.value, asterisks = T))   
  } else {
    out <- sprintf("t(%i) = %.2f, %s, d = %.2f, 95%% CI [%.2f, %.2f]",
                   t$parameter, t$statistic, round_p(t$p.value), 
                   ifelse(paired | is.null(y), cis$Standardized, cis$smd), 
                   cis$Lower, cis$Upper)    
  }
  if(means) {
    out <- paste0(out, sprintf(paste0(", M1 = %.", round, "f, M2 = %.", round, "f"), 
                               mean(x, na.rm = T), mean(y, na.rm = T)))
  }
  if(as.char) {
    out 
  } else {
    cat(out)  
  }
}



# function for comparison of correlations
compare_r <- function(x1, x2, y1, y2) {
    x <- cocor.indep.groups(cor(x1, x2, use = "na.or.complete"), 
                            cor(y1, y2, use = "na.or.complete"), 
                            sum(!is.na(x1) & !is.na(x2)), 
                            sum(!is.na(y1) & !is.na(y2)))
    CI <- x@zou2007$conf.int
    r <- function(x) sprintf("%.2f", x)
    cat("z = ", r(x@fisher1925$statistic), ", ", 
        round_p(x@fisher1925$p.value), ", ",
        "delta_r = ", r(x@diff), ", ",
        "95% CI = [", r(CI[1]), ", ",
        r(CI[2]), "]",
        sep = "")
}


# function for selecting "best" model
improve <- function(model) {
  drp <- drop1(model)
  wrst <- which(drp[,2] == max(drp[,2]))
  if(length(wrst) == 1 & (1 %in% wrst)) {
    return(model)
  } else {
    improve(update(model, formula(paste0(". ~ . - ", row.names(drp)[wrst[length(wrst)]])), evaluate = T))
  }
}


# function for computing coronbach's aplpha
p.alpha <- function(x) {
  shorten <- function(x) {
    s <- sprintf("%.2f", x)
    substr(s, 2, nchar(s))
  }
  alf <- psych::alpha(x, n.iter = 1000)
  sprintf("a = %s, 95%% CI [%s, %s]", shorten(alf$total[1]), 
          shorten(alf$boot.ci[1]), shorten(alf$boot.ci[3]))
}


# centering a variable to a range from -0.5 to 0.5
center <- function(x) {
  minimum <- min(x)
  maximum <- max(x)
  return((x - (minimum + maximum)/2)/(maximum - minimum))
}


# formatting percents
perc <- function(x) {round(mean(x), 2) * 100}


# statistics formatting
r <- function(x) sprintf("%.2f", x)
rci <- function(m, ci1, ci2) sprintf("%.2f [%.2f, %.2f]", m, ci1, ci2)
rsd <- function(m, sd) sprintf("%.2f (%.2f)", m, sd)
shorten <- function(x) {
  s <- sprintf("%.2f", x)
  if(x >= 0) {
    return(substr(s, 2, nchar(s)))
  } else {
    return(paste0("-", substr(s, 3, nchar(s))))
  }
}
rcor <- function(x, y) {
  ct <- cor.test(x, y)
  sprintf("%s [%s, %s]", 
          shorten(ct$estimate), 
          shorten(ct$conf.int[1]),
          shorten(ct$conf.int[2]))
}


# other
capitalize <- function(x) {
  paste0(toupper(substr(x, 1, 1)), substr(x, 2, nchar(x)))
}