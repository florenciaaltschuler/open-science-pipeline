bids <- read.table("Bids.txt", sep = "\t", head = T)
groups <- read.table("Groups.txt", sep = "\t", head = T)
sessions <- read.table("Sessions.txt", sep = "\t", head = T)
winners <- read.table("Winners.txt", sep = "\t", head = T)
participants <- read.table("Participants.txt", sep = "\t", head = T)

coding_bdm <- read.table("coding_bdm.txt", header = T, sep = "\t")
coding_auction <- read.table("coding_auction.txt", header = T, sep = "\t")
codes <- read.table("coding_codes.txt", header = T, sep = "\t")



source("helper.R")


#-------------------------------------------------------
# data
#-------------------------------------------------------
d1 <- read.table("Cheating 1 results.txt", sep = "\t", head = T, as.is = T)
d2 <- read.table("Cheating 2 results.txt", sep = "\t", head = T, as.is = T)
d3 <- read.table("Cheating 3 results.txt", sep = "\t", head = T, as.is = T)
d4 <- read.table("Cheating 4 results.txt", sep = "\t", head = T, as.is = T)
d5 <- read.table("Cheating 5 results.txt", sep = "\t", head = T, as.is = T)
d6 <- read.table("Cheating 6 results.txt", sep = "\t", head = T, as.is = T)
d7 <- read.table("Cheating 7 results.txt", sep = "\t", head = T, as.is = T)

# a technical bug froze the experiment for the participant, upon restarting s/he played the third round again, but the experiment could not proceed afterward
# the second time they played the third round is therefore excluded:
d3 <- d3[-as.numeric(rownames(d3[d3$id == "e422837e-197c-4f81-9f6f-7cd6501036de",]))[13:24],]

check_pred <- function(prediction, number) {
  ifelse(prediction == "odd", number %in% c(1,3,5), number %in% c(2,4,6))
}

d3$win <- ifelse(d3$version == "control", check_pred(d3$prediction, d3$roll), d3$report == "win")
d4$win <- ifelse(d4$version == "control", check_pred(d4$prediction, d4$roll), d4$report == "win")
d5$win <- ifelse(d5$version == "control", check_pred(d5$prediction, d5$roll), d5$report == "win")
d6$win <- ifelse(d6$version == "control", check_pred(d6$prediction, d6$roll), d6$report == "win")
d7$win <- ifelse(d7$version == "control", check_pred(d7$prediction, d7$roll), d7$report == "win")

d12 <- rbind(d1, d2)
d12 <- cbind(d12, win = ifelse(d12$version == "control", check_pred(d12$prediction, d12$roll), NA))

attention <- read.table("Attention checks results.txt", sep = "\t", head = T, as.is = T)
debrief1 <- read.table("Debriefing1 results.txt", sep = "\t", head = T, as.is = T, quote = "")
debrief2 <- read.table("Debriefing2 results.txt", sep = "\t", head = T, as.is = T, quote = "")
debrief3 <- read.table("Debriefing3 results.txt", sep = "\t", head = T, as.is = T, quote = "")
debrief4 <- read.table("Debriefing4 results.txt", sep = "\t", head = T, as.is = T, quote = "")
demo <- read.table("Demographics results.txt", sep = "\t", head = T, as.is = T)
dicelottery <- read.table("Dice Lottery results.txt", sep = "\t", head = T, as.is = T, quote = "")
ending <- read.table("Ending results.txt", sep = "\t", head = T, as.is = T)
hexaco <- read.table("Hexaco results.txt", sep = "\t", head = T, as.is = T, quote = "", encoding = "utf-8")
lottery <- read.table("Lottery results.txt", sep = "\t", head = T, as.is = T, quote = "")
prosociality <- read.table("Prosociality results.txt", sep = "\t", head = T, as.is = T, quote = "")
times <- read.table("Time results.txt", sep = "\t", head = T, as.is = T, quote = "")
auctioncontrol <- read.table("Auction Control Questions results.txt", sep = "\t", head = T, as.is = T, quote = "")
auctionresult <- read.table("Auction Result results.txt", sep = "\t", head = T, as.is = T, quote = "")
auction <- read.table("Auction results.txt", sep = "\t", head = T, as.is = T, quote = "")
bdmcontrol <- read.table("BDM Control Questions results.txt", sep = "\t", head = T, as.is = T, quote = "")
bdm <- read.table("BDM results.txt", sep = "\t", head = T, as.is = T, quote = "")
login <- read.table("Login results.txt", sep = "\t", head = T, as.is = T, quote = "")

#-------------------------------------------------------
# HEXACO
#-------------------------------------------------------
Honesty_Humility <- list(Sincerity = "6, 30R, 54",
                         Fairness = "12R, 36, 60R",
                         Greed_Avoidance = "18, 42R", 
                         Modesty = "24R, 48R") 

Emotionality <- list(Fearfulness = "5, 29, 53R", 
                     Anxiety = "11, 35R", 
                     Dependence = "17, 41R", 
                     Sentimentality = "23, 47, 59R")

Extraversion <- list(Social_Self_Esteem = "4, 28R, 52R", 
                     Social_Boldness = "10R, 34, 58",
                     Sociability = "16, 40",
                     Liveliness = "22, 46R")

Agreeableness <- list(Forgiveness = "3, 27",
                      Gentleness = "9R, 33, 51", 
                      Flexibility = "15R, 39, 57R", 
                      Patience = "21R, 45")

Conscientiousness <- list(Organization = "2, 26R", 
                          Diligence = "8, 32R", 
                          Perfectionism = "14R, 38, 50", 
                          Prudence = "20R, 44R, 56R")

Openness_to_Experience <- list(Aesthetic_Appreciation = "1R, 25", 
                               Inquisitiveness = "7, 31R", 
                               Creativity = "13, 37, 49R",
                               Unconventionality = "19R, 43, 55R") 

traits <- list(Honesty_Humility, Emotionality, Extraversion, Agreeableness,
               Conscientiousness, Openness_to_Experience)

hexaco_names <- c(c("Honesty_Humility", "Emotionality", "Extraversion", "Agreeableness",
                    "Conscientiousness", "Openness_to_Experience"),
                  names(unlist(traits)))

compute_hexaco <- function(answers) {
  avgs <- numeric(length = 30)
  tr_num <- 1
  sub_num <- 7
  for(trait in traits) {
    trait_tot <- 0
    for(sub in trait) {
      sub_tot <- 0
      questions <- unlist(strsplit(sub, ", "))
      for(q in questions) {
        if(length(grep("R", q)) == 0) {
          sub_tot <- sub_tot + answers[as.numeric(q)]
        } else {
          sub_tot <- sub_tot + 6 - answers[as.numeric(substr(q, 1, nchar(q)-1))]
        }
      }
      avgs[sub_num] <- sub_tot/length(questions)
      sub_num <- sub_num + 1
      trait_tot <- trait_tot + sub_tot
    }
    avgs[tr_num] <- trait_tot/10
    tr_num <- tr_num + 1
  }
  avgs    
}

hexaco_items <- read.table("hexaco2.txt", as.is = T, sep = "\t", quote = "")
hexaco_items[,1] <- gsub("[^[:alnum:]]", "", hexaco_items[,1])
hexaco$item <- gsub("[^[:alnum:]]", "", hexaco$item)
hexaco <- cbind(hexaco, item_num = unlist(sapply(hexaco$item, function(x) which(hexaco_items[,1] == x))))

hex_mat <- matrix(0, ncol = length(hexaco_names), nrow = length(unique(d1$id)))

#-------------------------------------------------------
# helper scales
#-------------------------------------------------------
compute_scale <- function(data, ids, items, reversed, endpoint, scales, names) {
  items <- gsub("[^[:alnum:]]", "", items)
  data$item <- gsub("[^[:alnum:]]", "", data$item)
  mat <- matrix(0, ncol = length(names), nrow = length(ids))
  for(id in 1:length(ids)) {
    for(sc in 1:length(names)) {
      temp <- 0
      for(it in scales[[sc]]) {
        ans <- data[data$item == items[it] & data$id == ids[id], "answer"]
        if(length(ans) == 0) {
          temp <- NA
          next
        }
        if(it %in% reversed) {ans <- endpoint + 1 - ans}
        temp <- temp + ans
      }
      mat[id, sc] <- temp / length(scales[[sc]])
    }
  }
  colnames(mat) <- names
  mat
}

#-------------------------------------------------------
# data munging
#-------------------------------------------------------
d <- data.frame(id = unique(d1$id), stringsAsFactors = F)
d <- cbind(d, reported = sapply(d$id, function(x) sum(d12$report[d12$id == x & d12$version == "treatment"] == "win")))
d <- cbind(d, control = sapply(d$id, function(x) sum(d12$win[d12$id == x & d12$version == "control"])))
d <- cbind(d, 
           highloss = sapply(d$id, function(x) startsWith(d1$condition[d1$id == x][1], "high")),
           info = unlist(sapply(d$id, function(x) endsWith(d1$condition[d1$id == x][1], "info")))
           )
d <- cbind(d,
           highloss.c = d$highloss - 0.5,
           info.c = d$info - 0.5,
           reported.c = scale(d$reported, scale = F))


fn <- function(x) {
  idx <- !(sapply(x, length))
  x[idx] <- NA
  x <- unlist(x)
  x
}

d <- cbind(d, 
           bdm3 = sapply(d$id, function(x) bdm$bid[bdm$id == x & bdm$block == 3]),
           bdm7 = fn(sapply(d$id, function(x) bdm$bid[bdm$id == x & bdm$block == 7])),
           auction4 = fn(sapply(d$id, function(x) auction$bid[auction$id == x & auction$block == 4])),
           prediction4 = fn(sapply(d$id, function(x) auction$prediction[auction$id == x & auction$block == 4])),
           auction5 = fn(sapply(d$id, function(x) auction$bid[auction$id == x & auction$block == 5])),
           prediction5 = fn(sapply(d$id, function(x) auction$prediction[auction$id == x & auction$block == 5])),
           auction6 = fn(sapply(d$id, function(x) auction$bid[auction$id == x & auction$block == 6])),
           prediction6 = fn(sapply(d$id, function(x) auction$prediction[auction$id == x & auction$block == 6])))

d <- cbind(d, 
           reported3 = sapply(d$id, function(x) sum(d3$win[d3$id == x])),
           reported4 = sapply(d$id, function(x) sum(d4$win[d4$id == x])),
           reported5 = sapply(d$id, function(x) sum(d5$win[d5$id == x])),
           reported6 = sapply(d$id, function(x) sum(d6$win[d6$id == x])),
           reported7 = sapply(d$id, function(x) sum(d7$win[d7$id == x])),
           after3 = sapply(d$id, function(x) d3$version[d3$id == x][1] == "treatment"),
           after4 = sapply(d$id, function(x) d4$version[d4$id == x][1] == "treatment"),
           after5 = sapply(d$id, function(x) d5$version[d5$id == x][1] == "treatment"),
           after6 = sapply(d$id, function(x) d6$version[d6$id == x][1] == "treatment"),
           after7 = sapply(d$id, function(x) d7$version[d7$id == x][1] == "treatment"))

d <- cbind(d, 
           auction4paid = fn(sapply(d$id, function(x) auctionresult$secondoffer[auctionresult$block == 4 & auctionresult$id == x])),
           auction5paid = fn(sapply(d$id, function(x) auctionresult$secondoffer[auctionresult$block == 5 & auctionresult$id == x])),
           auction6paid = fn(sapply(d$id, function(x) auctionresult$secondoffer[auctionresult$block == 6 & auctionresult$id == x])))

d <- cbind(d, 
           bdm3paid = fn(sapply(d$id, function(x) groups$bdm_one[groups$group_number == participants$group_number[participants$participant_id == x]])),
           bdm7paid = fn(sapply(d$id, function(x) groups$bdm_two[groups$group_number == participants$group_number[participants$participant_id == x]])))

d <- cbind(d,
           group = sapply(d$id, function(x) participants$group_number[participants$participant_id == x]))

d <- cbind(d, attention = fn(sapply(d$id, function(x) attention$correct[attention$id == x] > 1)),  
           risk_aversion = fn(sapply(d$id, function(x) length(grep("sure", lottery[lottery$id == x,]))))
           )

d <- cbind(d, 
           meanBDM = rowMeans(d[,c("bdm3", "bdm7")], na.rm = T),
           meanAuction = rowMeans(d[,c("auction4", "auction5", "auction6")], na.rm = T))


# participants with incomplete information:
id1 <- "913ea92d-73ae-4912-951e-e23b6838e8e4"
d[d$id == id1, c("reported6", "reported7")] <- NA
d[d$id == id1, "after6"] <- winners$winner[winners$block == 6 & winners$group_number == participants$group_number[participants$participant_id == id1]] == id1
d[d$id == id1, "auction6"] <- bids$bid[bids$block == 6 & bids$participant_id == id1]
d[d$id == id1, "auction6paid"] <- winners$secondoffer[winners$block == 6 & winners$group_number == participants$group_number[participants$participant_id == id1]]
id2 <- "2dbe7c8f-2243-4fc3-8a82-9d08d2e75eef"
d[d$id == id2, c("reported6", "reported7")] <- NA
d[d$id == id2, "after6"] <- winners$winner[winners$block == 6 & winners$group_number == participants$group_number[participants$participant_id == id2]] == id2
d[d$id == id2, "auction6"] <- bids$bid[bids$block == 6 & bids$participant_id == id2]
d[d$id == id2, "auction6paid"] <- winners$secondoffer[winners$block == 6 & winners$group_number == participants$group_number[participants$participant_id == id2]]
# participant who did not finish the experiment
id3 <- "e422837e-197c-4f81-9f6f-7cd6501036de"
d[d$id == id3, c("reported4", "reported5", "reported6", "reported7")] <- NA
winners[winners$wins < 0, c("wins", "reward", "charity")] <- c(NA, NA, NA)
# and his/her group members
group3 <- d[d$id == "e422837e-197c-4f81-9f6f-7cd6501036de", "group"]
d[d$group == group3, c("reported5", "reported6", "reported7", "bdm7", "auction5", "auction6", "prediction5", "prediction6", "after5", "after6", "after7", "auction5paid", "auction6paid")] <- NA


# hexaco
for(i in 1:nrow(d)) {
  temp <- hexaco[hexaco$id == d$id[i],]
  temp <- temp[order(temp$item_num),] 
  hex_mat[i,] <- compute_hexaco(temp$answer)
}
colnames(hex_mat) <- hexaco_names
d <- cbind(d, hex_mat)


d <- cbind(d, prosociality = fn(sapply(d$id, function(x) mean(prosociality$answer[prosociality$id == x]))))
d$prosociality.c <- scale(d$prosociality, scale = F)

d <- cbind(d, control_first = sapply(d$id, function(x) d1[d1$id == x, "version"][1] == "control"))
d <- cbind(d, Honesty_Humility.c = scale(d$Honesty_Humility, scale = F))
d <- cbind(d,
           winner.pred.4 = sapply(d$group, function(x) winners$wins[winners$block == 4 & winners$group_number == x]),
           winner.pred.5 = sapply(d$group, function(x) winners$wins[winners$block == 5 & winners$group_number == x]))
d$winner.pred.4.z <- scale(d$winner.pred.4)
d$winner.pred.5.z <- scale(d$winner.pred.5)

# task perception
d <- merge(d, debrief2, by = "id", all.x = T)
d <- merge(d, debrief3, by = "id", all.x = T)
d <- merge(d, debrief4, by = "id", all.x = T)
scale1 <- c("Vůbec ne" = 1, "Jen trochu" = 2, "Do určité míry" = 3, "Spíše hodně" = 4, "Velmi" = 5)
d$others_charity_interest <- scale1[d$others_charity_interest]
d$you_charity_interest<- scale1[d$you_charity_interest]
d$aware_cheating <- ifelse(d$aware_cheating == "Ano, napadlo mě to", 1, 0)
d$aware_preventing_cheating <- ifelse(d$aware_preventing_cheating == "Ano, napadlo mě to", 1, 0)
d$aware_preventing_loss <- ifelse(d$aware_preventing_loss == "Ano, napadlo mě to", 1, 0)


# long format
long <- pivot_longer(d, cols = c("bdm3", "auction4", "auction5", "auction6", "bdm7"), names_to = "block", values_to = "bid") 
long$h3 <- ifelse(long$block == "auction4", 0.5, -0.5)
long$bid.z <- numeric(length = nrow(long))
for(r in c("bdm3", "auction4", "auction5", "auction6", "bdm7")) {
  long$bid.z[long$block == r] <- scale(long$bid[long$block == r])  
}
long$winner.pred <- numeric(length = nrow(long))
long$winner.pred <- NA
long$winner.pred[long$block == "auction5"] <- long$winner.pred.4[long$block == "auction5"]
long$winner.pred[long$block == "auction6"] <- long$winner.pred.5[long$block == "auction6"]
long$winner.pred.z <- numeric(length = nrow(long))
long$winner.pred.z <- NA
long$winner.pred.z[long$block == "auction5"] <- long$winner.pred.4.z[long$block == "auction5"]
long$winner.pred.z[long$block == "auction6"] <- long$winner.pred.5.z[long$block == "auction6"]

# coding of an open question
codes$bdm <- numeric(length = nrow(codes))
codes$auction <- numeric(length = nrow(codes))
codes$bdm_perc <- numeric(length = nrow(codes))
codes$auction_perc <- numeric(length = nrow(codes))
for(i in 1:nrow(codes)) {
  codes$bdm[i] <- length(grep(pattern = codes$Coding.scheme[i], x = coding_bdm$coding, ignore.case = T))
  codes$auction[i] <- length(grep(pattern = codes$Coding.scheme[i], x = coding_auction$coding, ignore.case = T))
  codes$bdm_perc[i] <- round(length(grep(pattern = codes$Coding.scheme[i], x = coding_bdm$coding, ignore.case = T)) * 100 / nrow(coding_bdm), 1)
  codes$auction_perc[i] <- round(length(grep(pattern = codes$Coding.scheme[i], x = coding_auction$coding, ignore.case = T)) * 100 / nrow(coding_auction), 1)
}


#-------------------------------------------------------
# demographics
#-------------------------------------------------------
power.t.test(n = nrow(d)/2, sig.level = .05, power = .80, type = "two.sample")
pwr.r.test(n = nrow(d), sig.level = .05, power = .80)

table(demo$sex)/nrow(demo)
median(demo$age)
IQR(demo$age)
table(demo$student)/nrow(demo)
table(demo$field)/sum(demo$student == "student")
mean(participants$reward[participants$reward > 0])


mean(table(sapply(unique(d$group), function(x) groups$session[groups$group_number == x])))
median(table(sapply(unique(d$group), function(x) groups$session[groups$group_number == x])))
sum(table(sapply(unique(d$group), function(x) groups$session[groups$group_number == x])) == 1)



#-------------------------------------------------------
# descriptives and other analysis
#-------------------------------------------------------
# descriptive statistics Table
preds <- c("reported", "meanBDM", "meanAuction", "Honesty_Humility", "Emotionality", "Extraversion", "Agreeableness",
           "Conscientiousness", "Openness_to_Experience", "risk_aversion", "prosociality")
apa.cor.table(apply(d[,preds], 2, as.numeric), 
              filename = "Table1.doc", table.number = NA,
              show.conf.interval = FALSE, landscape = TRUE)

# conservative estimate of the number of cheaters
estimateCheaters <- function(x) {
  sorted_data <- sort(x)
  ecdf_observed <- ecdf(sorted_data)
  theoretical_cdf <- pbinom(sorted_data, size = 12, prob = 0.5)
  d_plus <- max(theoretical_cdf - ecdf_observed(sorted_data)) 
  d_minus <- max(ecdf_observed(sorted_data) - theoretical_cdf)
  print(d_plus)
  print(d_minus)
}

estimateCheaters(d$reported3[d$after3])
estimateCheaters(d$reported4[d$after4])
estimateCheaters(d$reported5[d$after5])
estimateCheaters(d$reported6[d$after6])
estimateCheaters(d$reported7[d$after7])


# cheating after paying money to play the after version
pt.test(d$reported3[d$after3], d$reported[d$after3], paired = T, means = T)
t3 <- t.test(d$reported3[d$after3], d$reported[d$after3], paired = T)
ci.sm(ncp = t3$statistic, N = t3$parameter + 1)
pt.test(d$reported4[d$after4], d$reported[d$after4], paired = T, means = T)
pt.test(d$reported5[d$after5], d$reported[d$after5], paired = T, means = T)
t.test(d$reported5[d$after5], d$reported[d$after5], paired = T)
pt.test(d$reported6[d$after6], d$reported[d$after6], paired = T, means = T)
t6 <- t.test(d$reported6[d$after6], d$reported[d$after6], paired = T)
ci.sm(ncp = t6$statistic, N = t6$parameter + 1)
pt.test(d$reported7[d$after7], d$reported[d$after7], paired = T, means = T)

# increase in WTP
t.test(d$auction4, d$bdm3, paired = T)
t.test(d$auction5, d$auction4, paired = T)
t.test(d$auction6, d$auction5, paired = T)
t.test(d$bdm7, d$auction6, paired = T)
pt.test(d$bdm7, d$auction6, paired = T, means = T)

# benevolent bidders
sum(d$meanBDM == 0)
sum(d$meanBDM < 10)
sum(d$meanAuction[d$meanBDM < 10] < 10)
sum(d$meanAuction[d$meanBDM < 10] < 50)
d$meanAuction[d$meanBDM < 10][d$meanAuction[d$meanBDM < 10] >= 50]
sum(d$meanAuction[d$meanBDM < 10] >= 50) / sum(!is.na(d$meanAuction))
sum(d$after4[d$meanBDM < 10])
sum(d$after5[d$meanBDM < 10])
sum(d$after6[d$meanBDM < 10])
d$reported4[d$after4 & d$meanBDM < 10]
pt.test(d$reported[d$meanAuction >= 50 & d$meanBDM < 10], d$reported[d$meanAuction < 50 | d$meanBDM >= 10], means = T)

# all in one
long$bdm <- startsWith(long$block, "bdm")*1
long$bdm.c <- long$bdm - 0.4
long$blocknum <- as.numeric(substr(long$block, nchar(long$block), nchar(long$block)))
long$blocknum.c <- long$blocknum - 5
long$fivesix <- (long$blocknum == 5 | long$blocknum == 6)*1
long$fivesix.c <- long$fivesix - 0.4

mod1 <- lmer(bid ~ reported.c*highloss.c + bdm.c*prosociality.c + bdm.c:reported.c + blocknum.c + fivesix.c:info.c + info.c + (bdm.c + blocknum.c|id), data = long)
summary(mod1)

tab_model(mod1,
          collapse.ci = TRUE,
          show.ngroups = FALSE,
          show.re.var = FALSE, 
          show.icc = FALSE,
          show.obs = FALSE,
          pred.labels = c("(Intercept)", "Baseline cheating", "High loss", "BDM", "Prosociality",
                          "Round", "Information", "Baseline * High loss", "BDM * Prosociality", "Baseline * BDM", 
                          "Rounds 5 or 6 * Information"),
          dv.labels = c("Willingness to pay"),
          file = "Table2.html")

# risk aversion
m.ra3 <- lm(bdm3 ~ risk_aversion + highloss.c, data = d)
m.ra4 <- lm(auction4 ~ risk_aversion + highloss.c, data = d)
m.ra5 <- lm(auction5 ~ risk_aversion + highloss.c, data = d)
m.ra6 <- lm(auction6 ~ risk_aversion + highloss.c, data = d)
m.ra7 <- lm(bdm7 ~ risk_aversion + highloss.c, data = d)
summary(m.ra3)
summary(m.ra4)
summary(m.ra5)
summary(m.ra6)
summary(m.ra7)


#-------------------------------------------------------
# decision making
#-------------------------------------------------------
debriefvariables <- c('bdm_reward', 'bdm_charity_loss', 'bdm_charity_loss_others', 'bdm_others_bids', 'bdm_others_prediction', 'bdm_fun', 'bdm_ease', 'bdm_reward_influence', 'bdm_charity_loss_influence', 'bdm_winner', 'bdm_overcome_others', 'auction_reward', 'auction_charity_loss', 'auction_charity_loss_others', 'auction_others_bids', 'auction_others_prediction', 'auction_fun', 'auction_ease', 'auction_reward_influence', 'auction_charity_loss_influence', 'auction_winner', 'auction_overcome_others', 'bdm_unfair', 'bdm_risky', 'bdm_not_understood', 'bdm_complicated', 'auction_unfair', 'auction_risky', 'auction_not_understood', 'auction_complicated', 'others_charity_interest', 'you_charity_interest', 'aware_cheating', 'aware_preventing_cheating', 'aware_preventing_loss')

bdmvariables <- c('bdm_reward', 'bdm_charity_loss', 'bdm_charity_loss_others', 'bdm_others_bids', 'bdm_others_prediction', 'bdm_fun', 'bdm_ease', 'bdm_reward_influence', 'bdm_charity_loss_influence', 'bdm_winner', 'bdm_overcome_others', 'bdm_unfair', 'bdm_risky', 'bdm_not_understood', 'bdm_complicated')

auctionvariables <- c('auction_reward', 'auction_charity_loss', 'auction_charity_loss_others', 'auction_others_bids', 'auction_others_prediction', 'auction_fun', 'auction_ease', 'auction_reward_influence', 'auction_charity_loss_influence', 'auction_winner', 'auction_overcome_others', 'auction_unfair', 'auction_risky', 'auction_not_understood', 'auction_complicated')

dimensionsEN <- c("your expected monetary earnings",
                   "the loss of money I may cause to charity",
                   "the loss of money that other members of the group may cause the charity",
                   "the amount of money that will be offered by other members of the group",
                   "the number of correct predictions made by other group members in the AFTER version",
                   "how much fun it is to play both versions of the task",
                   "how easy it is to play both versions of the task",
                   "ability to influence the size of one's monetary earnings",
                   "ability to influence the size of the loss of charity",
                   "aspiration to be a winner",
                   "aspiration to outperform others",
                   "unfair",
                   "risky",
                   "did not understand",
                   "complicated")

tab4 <- data.frame(Dimension = dimensionsEN,
                   MBDM = round(colMeans(d[,bdmvariables], na.rm = T), 2),
                   SDBDM = round(apply(d[,bdmvariables], 2, function(x) sd(x, na.rm = T)), 2),
                   corBaselineBDM = apply(d[,bdmvariables], 2, function(x) p.cor(x, d$reported, use = "pairwise.complete.obs", sparse = T)),
                   corBDM = apply(d[,bdmvariables], 2, function(x) p.cor(x, d$meanBDM, use = "pairwise.complete.obs", sparse = T)),
                   Mauction = round(colMeans(d[,auctionvariables], na.rm = T), 2),
                   SDauction = round(apply(d[,auctionvariables], 2, function(x) sd(x, na.rm = T)), 2),
                   corBaselineAuction = apply(d[,auctionvariables], 2, function(x) p.cor(x, d$reported, use = "pairwise.complete.obs", sparse = T)),
                   corAuction = apply(d[,auctionvariables], 2, function(x) p.cor(x, d$meanAuction, use = "pairwise.complete.obs", sparse = T)),
                   tTestD = sapply(1:length(bdmvariables), function(x) pt.test(d[,auctionvariables[x]], d[,bdmvariables[x]], paired = T, as.char = T, sparse = T)))
print(nice_table(tab4), preview = "docx")


round(colMeans(d[,debriefvariables], na.rm = T), 2)
pt.test(d$others_charity_interest, d$you_charity_interest, paired = T, means = T)
p.cor(d$you_charity_interest, d$reported)
p.cor(d$you_charity_interest, d$meanBDM)
p.cor(d$you_charity_interest, d$meanAuction)


#-------------------------------------------------------
# pre-registered analysis
#-------------------------------------------------------
# H1 will be tested using linear regression with the willingness to pay in the third (H1a) and fourth (H1b) round as the dependent variable and the baseline measure of cheating as the predictor of interest. 
# shown in figure, so these tests are not reported in the text of the manuscript
m1a <- lm(d$bdm3 ~ d$reported)
summary(m1a)
results(m1a, 2, family = "linear", rounding = 3)

m1b <- lm(d$auction4 ~ d$reported)
summary(m1b)
results(m1b, 2, family = "linear", rounding = 2)

# H2 will be tested using linear regression with the bid in the auction in the fourth round as the dependent variable and the interaction of loss condition with baseline measure of cheating as the predictor of interest. Main effects for the two predictor variables will be also included in the model. 

m2 <- lm(auction4 ~ highloss.c*reported.c, data = d)
summary(m2)
results(m2, 4, family = "linear", rounding = 1)

m2a <- lm(auction4 ~ reported.c, data = d, subset = d$highloss)
summary(m2a) 
results(m2a, 2, family = "linear", rounding = 1)

m2b <- lm(auction4 ~ reported.c, data = d, subset = !d$highloss)
summary(m2b) 
results(m2b, 2, family = "linear", rounding = 1)

# H3 will be tested using a linear mixed-effect model with the willingness to pay in the third and fourth round as the dependent variable, round (i.e., auction vs. BDM) and prosociality as covariates and their interaction as the predictor of interest. Loss condition will be also included in the model as a covariate. Random intercepts and random slopes for round for participants will be included in the model.

m3 <- lmer(bid ~ h3*prosociality.c + highloss.c + (1|id), data = long, subset = long$block == "bdm3" | long$block == "auction4")
# not possible to include random slopes, because the parameters are unidentifiable
summary(m3)
results(m3, 5, family = "linear", rounding = 3)

# H4 will be tested with the same model as H3, but the loss condition will be included in the model alongside its two- and three-way interactions with the other predictors. The three way interaction will be used to test the prediction.

m4 <- lmer(bid ~ h3*prosociality.c*highloss.c + (1|id), data = long, subset = long$block == "bdm3" | long$block == "auction4")
summary(m4)
results(m4, 8, family = "linear", rounding = 3)
 
# H5 will be tested using the same model as H3, but the baseline measure of cheating will be used instead of prosociality in the model.

m5 <- lmer(bid ~ h3*reported.c + highloss.c + (1|id), data = long, subset = long$block == "bdm3" | long$block == "auction4")
summary(m5)
results(m5, 5, family = "linear", rounding = 3)

# H6 will be tested using a linear regression model where the number of correct predictions reported in the fourth round by the participant who will win the auction for the AFTER version of the task will serve as the dependent variable. The bid of the participants and loss condition will be included in the model as covariates and the second highest bid as the predictor of interest.

m6 <- lm(reported4 ~ auction4 + highloss.c + auction4paid, data = d, subset = d$after4)
summary(m6)
results(m6, 4, family = "linear", rounding = 3) 

m6.bdm3 <- lm(reported3 ~ bdm3 + highloss.c + bdm3paid, data = d, subset = d$after3)
summary(m6.bdm3)
results(m6.bdm3, 4, family = "linear", rounding = 3) 

m6.bdm7 <- lm(reported7 ~ bdm7 + highloss.c + bdm7paid, data = d, subset = d$after7)
summary(m6.bdm7)
results(m6.bdm7, 4, family = "linear", rounding = 3) 

m6.auction5 <- lm(reported5 ~ auction5 + highloss.c + auction5paid, data = d, subset = d$after5)
summary(m6.auction5)
results(m6.auction5, 4, family = "linear", rounding = 3) 

m6.auction6 <- lm(reported6 ~ auction6 + highloss.c + auction6paid, data = d, subset = d$after6)
summary(m6.auction6)
results(m6.auction6, 4, family = "linear", rounding = 3) 

# H7 will be tested using a linear regression with the willingness to pay in the third (H7a) and fourth (H7b) round as the dependent variable, honesty-humility as the predictor of interest and loss condition as a covariate.

m7a <- lm(bdm3 ~ Honesty_Humility + highloss.c, data = d)
summary(m7a)
results(m7a, 2, family = "linear", rounding = 2)

m7b <- lm(auction4 ~ Honesty_Humility + highloss.c, data = d)
summary(m7b)
results(m7b, 2, family = "linear", rounding = 2)

m7c <- lm(auction5 ~ Honesty_Humility + highloss.c, data = d)
summary(m7c)
results(m7c, 2, family = "linear", rounding = 2)

m7d <- lm(auction6 ~ Honesty_Humility + highloss.c, data = d)
summary(m7d)
results(m7d, 2, family = "linear", rounding = 2)

m7e <- lm(bdm7 ~ Honesty_Humility + highloss.c, data = d)
summary(m7e)
results(m7e, 2, family = "linear", rounding = 2)

# H8 will be tested using a linear mixed-effect regression with the willingness to pay in the third and fourth round as the dependent variable and honesty-humility and its interaction with round as predictors. The interaction will be of the primary interest. Loss condition will be included in the model as a covariate. The willingness to pay will be standardized for each of the rounds before analysis. Random intercepts for participants will be included in the model.

m8 <- lmer(bid.z ~ h3*Honesty_Humility.c + highloss.c + (1|id), data = long, subset = long$block == "bdm3" | long$block == "auction4")
summary(m8)
results(m8, 5, family = "linear", rounding = 3)

# H9 will be tested using a linear mixed-effect regression model with the bids in fifth and sixth round as the dependent variable, round and loss condition as covariates and information condition as the predictor of interest. The model will include random intercepts for groups and participants.

m9 <- lmer(bid ~ block + highloss.c + info + (1|group/id), data = long, subset = long$block == "auction5" | long$block == "auction6")
summary(m9)
results(m9, 4, family = "linear", rounding = 2)

# H10 will be analyzed using the same model as H9, but the number of correct predictions of the group member who won the bid in the previous round of the auction will serve as an additional predictor by which the H10 will be tested.

m10 <- lmer(bid ~ block + highloss.c + info.c*winner.pred.z + (1|group/id), data = long, subset = long$block == "auction5" | long$block == "auction6")
# the interaction with the information condition is actually of interest here
summary(m10)
results(m10, 6, family = "linear", rounding = 2) 

# H11 will be tested using a linear regression with the bid in the fourth round as the dependent variable, the estimate of the number of reported correct predictions as the predictor of interest and loss condition as well as its interaction with the estimate as covariates.

m11 <- lm(auction4 ~ prediction4*highloss.c, data = d)
summary(m11)
results(m11, 2, family = "linear", rounding = 2) 

# H12 will be tested using linear mixed-effect regression models with the number of reported correct predictions in the AFTER version of the task in fourth to sixth rounds as the dependent variable and loss and information conditions as well as their interaction as predictors. Random intercept for groups will be included in the model. The main effect of the loss condition will be of primary interest.
winners$condition <- sapply(winners$group_number, function(x) groups$condition[groups$group_number == x])
winners$highloss <- startsWith(winners$condition, "high")
winners$info <- endsWith(winners$condition, "info")
winners$highloss.c = winners$highloss - 0.5
winners$info.c = winners$info - 0.5
m12 <- lmer(wins ~ block + highloss.c*info.c + (1|group_number), data = winners)
summary(m12)
results(m12, 3, family = "linear", rounding = 3) 

# H13 will be tested using linear mixed-effect regression models with the number of reported correct predictions in the AFTER version of the task in fifth and sixth rounds as the dependent variable and loss and information conditions as well as their interaction as predictors. Random intercept for groups will be included in the model. The main effect of the information condition will be of primary interest.
m13 <- lmer(wins ~ block + highloss.c*info.c + (1|group_number), data = winners, subset = winners$block > 4)
summary(m13)
results(m13, 4, family = "linear", rounding = 3) 


#-------------------------------------------------------
# figures
#-------------------------------------------------------
addPoints <- function(data, offset = 0, color = "black") {
  for(i in 0:12) {
    x <- i + offset
    occur <- sum(d$reported == i)
    if(occur > 10) {
      t <- t.test(data[d$reported == i])
      points(x, t$estimate, pch = 16, cex = 1.8, col = color)
      lines(c(x, x), c(t$conf.int[1], t$conf.int[2]), lwd = 5, col = color, lend = 2)  
    } else {
      if(occur != 0) {
        points(x, mean(data[d$reported == i], na.rm = T), pch = 16, cex = 1.8, col = color)
      }
    }
  }
}


png("Fig3.png", width = 2100, height = 950, pointsize = 24)

par(las = 1, cex.axis = 1.5, cex.lab = 1.55, oma = c(0,0,0,0)) #

layout(matrix(1:2, 1, 2, byrow = TRUE), widths = c(12,1))

par(las = 1, cex.axis = 1.35, cex.lab = 1.55, mar = c(5, 6, 1, 0.1))
plot(0,0,
     ylim = c(0,300), xlim = c(0,12),
     xlab = "", ylab = "",
     #xaxs = "i", yaxs = "i",
     main = "", 
     type = "n"#,
     #xaxt = "n", yaxt = "n",
     #axes = F
)

axis(side = 1, at = seq(1,11,2))

addPoints(d$bdm3, -0.3)
addPoints(d$auction4, -0.15, "red")
addPoints(d$auction5, 0, "red")
addPoints(d$auction6, 0.15, "red")
addPoints(d$bdm7, 0.3)

mtext("Baseline measure of cheating", side = 1, line = 3.5, at = 6.5, cex = 2)
mtext("Willingness to pay", side = 2, line = 4, at = 150, cex = 2, las = 3)

points(0, 280, pch = 16, cex = 1.8, col = "red")
points(0, 260, pch = 16, cex = 1.8, col = "black")
text(x = 0.15, y = 280, labels = "Auction", cex = 1.5, adj = c(0,0.5))
text(x = 0.15, y = 260, labels = "BDM", cex = 1.5, adj = c(0,0.5))

# averages
par(las = 1, cex.axis = 1.35, cex.lab = 1.55, mar = c(5, 0.1, 1, 1))
plot(0,0,
     ylim = c(0,300), xlim = c(0,5),
     xlab = "", ylab = "",
     #xaxs = "i", yaxs = "i",
     main = "", 
     type = "n",
     xaxt = "n", yaxt = "n"#,
     #axes = F
)
colors <- c("black", rep("red", 3), "black")
columns <- c("bdm3", "auction4", "auction5", "auction6", "bdm7") 
for(i in 1:5) {
  x <- i - 0.5
  t <- t.test(d[,columns[i]])
  points(x, t$estimate, pch = 16, cex = 1.8, col = colors[i])
  lines(c(x, x), c(t$conf.int[1], t$conf.int[2]), lwd = 5, col = colors[i], lend = 2)  
} 
mtext("Average", side = 1, line = 3.5, at = 2.5, cex = 2)

dev.off()

par(mfrow=c(1,1))



#---------------------------------------------------------------------------------------------------------------------
shadowtext <- function(x, y=NULL, labels, col='white', bg='black', 
                       theta= seq(0, 2*pi, length.out=50), r=0.1, ... ) {
  
  xy <- xy.coords(x,y)
  xo <- r*strwidth('A')
  yo <- r*strheight('A')
  
  # draw background text with small shift in x and y in background colour
  for (i in theta) {
    text( xy$x + cos(i)*xo, xy$y + sin(i)*yo, labels, col=bg, ... )
  }
  # draw actual text in exact xy position in foreground colour
  text(xy$x, xy$y, labels, col=col, ... )
}
addhist <- function(vec, n, group = "", maxy = 0.71) {
  plot(0,0,
       ylim = c(0, maxy), xlim = c(-0.5, n + 0.5),
       xlab = "", ylab = "",
       xaxs = "i", yaxs = "i",
       main = "", 
       type = "n",
       xaxt = "n", yaxt = "n",
       axes = F
  )  
  for(i in seq(0, maxy, 0.1)) {
    abline(h = i, lty = 3, col = "grey")
  }
  abline(v = n/2, lty = 2)
  for(i in 0:n) {
    par(xpd = TRUE)
    rect(xleft = i - 0.5, ybottom = 0, xright = i + 0.5, ytop = sum(vec == i, na.rm = T)/sum(!is.na(vec)), col = "grey")
    par(xpd = FALSE)
    points(x = i, y = dbinom(x = i, size = n, prob = 0.5), pch = 4, cex = 0.8, lwd = 2)
  }
  axis(side = 2, at = seq(0, maxy, 0.1))
  points(x = mean(vec, na.rm = T), y = maxy - 0.04, pch = 16, cex = 2, col = "black")
  cis <- t.test(vec)$conf.int
  lines(x = cis, y = rep(maxy - 0.04, 2), lwd = 3, lend = 2, col = "black")
  shadowtext(x = -0.2, y = maxy - 0.07, labels = group, adj = 0, cex = 1.8, col = "black", bg = "white")
}
addCIs <- function(vec) {
  y <- par("usr")[4] - 0.08
  points(x = mean(vec, na.rm = T), y = y, pch = 16, cex = 2, col = "grey")
  cis <- t.test(vec)$conf.int
  lines(x = cis, y = rep(y, 2), lwd = 3, lend = 2, col = "grey")
}


#----

png("Fig2.png", width = 1250, height = 1850, pointsize = 24)
par(las = 1, cex.axis = 1.5, cex.lab = 1.55, oma = c(4,3,0,0))
layout(matrix(1:9, 9, 1, byrow = TRUE), heights = c(1, rep(3,2), 1, rep(3,5)))
par(mar = c(0,0,0,0))
plot(0,0, type="n", axes = F, xlim = c(0,1), ylim = c(0,1))
text(labels = "Baseline", x = 0.5, y = 0.5, cex = 2.2)
par(mar = c(1,3,0.5,1))
addhist(d$reported[d$highloss], 12, sprintf("High loss, n = %i", sum(d$highloss)))
addhist(d$reported[!d$highloss], 12, sprintf("Low loss, n = %i", sum(!d$highloss)))
par(mar = c(0,0,0,0))
plot(0,0, type="n", axes = F, xlim = c(0,1), ylim = c(0,1))
text(labels = "After payment", x = 0.5, y = 0.5, cex = 2.2)
par(mar = c(1,3,0.5,1))
addhist(d$reported3[d$after3], 12, sprintf("After BDM, 3rd block, n = %i", sum(d$after3)))
addCIs(d$reported[d$after3])
addhist(d$reported4[d$after4], 12, sprintf("After Auction, 4th block, n = %i", sum(d$after4, na.rm = T)))
addCIs(d$reported[d$after4])
mtext(text = "Probability", side = 2, line = 3.7, at = 0.6, cex = 1.5, las = 3)
addhist(d$reported5[d$after5], 12, sprintf("After Auction, 5th block, n = %i", sum(d$after5, na.rm = T)))
addCIs(d$reported[d$after5])
addhist(d$reported6[d$after6], 12, sprintf("After Auction, 6th block, n = %i", sum(d$after6, na.rm = T)))
addCIs(d$reported[d$after6])
addhist(d$reported7[d$after7], 12, sprintf("After BDM, 7th block, n = %i", sum(d$after7, na.rm = T)))
addCIs(d$reported[d$after7])
axis(side = 1, at = 0:12)
mtext(text = "Number of reported correct predictions", side = 1, line = 3.2, at = 6, cex = 1.5)
dev.off()


#---------------------------------------------------------------------------------------------------------------------

png("Fig4.png", width = 1450, height = 2050, pointsize = 24)

preds <- c("Honesty_Humility", "Emotionality", "Extraversion", "Agreeableness",
           "Conscientiousness", "Openness_to_Experience", "risk_aversion", "prosociality", "reported",
           "highloss.c", "info.c")
pnames <- c("Honesty-Humility", "Emotionality", "Extraversion",
            "Agreeableness", "Conscientiousness", "Openness to experience", "Risk aversion", "Prosociality", "Baseline cheating",
            "High loss condition", "Information condition")
dvs<- c("bdm3", "auction4", "auction5", "auction6", "bdm7")
cols <- c("black", "red", "red", "red", "black")

par(las = 1, cex.axis = 1.35, cex.lab = 1.55, mar = c(1, 16, 6, 1))
plot(0,0,
     ylim = c(0,length(preds)), xlim = c(-0.5, 0.5),
     xlab = "", ylab = "",
     xaxs = "i", yaxs = "i",
     main = "",
     type = "n",
     xaxt = "n", yaxt = "n",
     axes = F
)
axis(side = 3, at = seq(-0.5,0.5,0.1), labels = seq(-0.5,0.5,0.1), cex.axis = 1)
abline(v = 0, lwd = 2, lty = 3)
for(i in 1:length(preds)) {
  y <- length(preds)- i + 0.5
  mtext(text = pnames[i], side = 2, line = 2.5, at = y, cex = 1.5, las = 1)
    for(j in 1:length(dvs)) {
    y <- length(preds)- i + 0.5 - (j-1)*0.15 + (length(dvs) - 1)*0.075
    sci <- spearman.ci(d[d$attention, preds[i]], d[d$attention, dvs[j]], nrep = 1000)
    points(sci$estimate, y, pch = 16, cex = 2, col = cols[j])
    lines(c(sci$conf.int[1], sci$conf.int[2]), c(y, y), lend = 2, lwd = 3, col = cols[j])  
  }
}
mtext(text = "Correlation with the willingness to pay", side = 3, line = 3, at = 0, cex = 2)

dev.off()


#-------------------------------------------------------
# table 1
#-------------------------------------------------------
tab1 <- data.frame("Number of correct predictions" = c("Participant's gain", "Charity's loss in the low-loss condition", "Charity's loss in the high-loss condition"),
                   '1 to 9' = c("5 to 45", "0", "0"),
                   '10' = c(50,25,100),
                   '11' = c(55,50,200),
                   '12' = c(60,75,300))
print(nice_table(tab1), preview = "docx")



#---------------------------
# FIGURES FOR OSF

addPoints2 <- function(data, offset = 0, color = "black") {
  for(i in 0:12) {
    x <- i + offset
    occur <- sum(d$reported == i)
    if(occur > 10) {
      t <- t.test(data[d$reported == i])
      points(x, t$estimate, pch = 16, cex = 1.8, col = color)
      lines(c(x, x), c(t$conf.int[1], t$conf.int[2]), lwd = 5, col = color, lend = 2)  
      text(x = x, y = 250, labels = sprintf("%.1f [%.1f, %.1f]", t$estimate, t$conf.int[1], t$conf.int[2]), srt = 90, adj = 0, cex = 0.6)
    } else {
      if(occur != 0) {
        points(x, mean(data[d$reported == i], na.rm = T), pch = 16, cex = 1.8, col = color)
        text(x = x, y = 250, labels = sprintf("%.1f", mean(data[d$reported == i])), srt = 90, adj = 0, cex = 0.6)
      }
    }
  }
}

png("Fig3appendix.png", width = 2100, height = 950, pointsize = 24)

par(las = 1, cex.axis = 1.5, cex.lab = 1.55, oma = c(0,0,0,0)) #

layout(matrix(1:2, 1, 2, byrow = TRUE), widths = c(12,1))

par(las = 1, cex.axis = 1.35, cex.lab = 1.55, mar = c(5, 6, 1, 0.1))
plot(0,0,
     ylim = c(0,300), xlim = c(0,12),
     xlab = "", ylab = "",
     #xaxs = "i", yaxs = "i",
     main = "", 
     type = "n"#,
     #xaxt = "n", yaxt = "n",
     #axes = F
)

axis(side = 1, at = seq(1,11,2))

addPoints2(d$bdm3, -0.3)
addPoints2(d$auction4, -0.15, "red")
addPoints2(d$auction5, 0, "red")
addPoints2(d$auction6, 0.15, "red")
addPoints2(d$bdm7, 0.3)

mtext("Baseline measure of cheating", side = 1, line = 3.5, at = 6.5, cex = 2)
mtext("Willingness to pay", side = 2, line = 4, at = 150, cex = 2, las = 3)

points(0, 240, pch = 16, cex = 1.8, col = "red")
points(0, 220, pch = 16, cex = 1.8, col = "black")
text(x = 0.15, y = 240, labels = "Auction", cex = 1.5, adj = c(0,0.5))
text(x = 0.15, y = 220, labels = "BDM", cex = 1.5, adj = c(0,0.5))

# averages
par(las = 1, cex.axis = 1.35, cex.lab = 1.55, mar = c(5, 0.1, 1, 1))
plot(0,0,
     ylim = c(0,300), xlim = c(0,5),
     xlab = "", ylab = "",
     #xaxs = "i", yaxs = "i",
     main = "", 
     type = "n",
     xaxt = "n", yaxt = "n"#,
     #axes = F
)
colors <- c("black", rep("red", 3), "black")
columns <- c("bdm3", "auction4", "auction5", "auction6", "bdm7") 
for(i in 1:5) {
  x <- i - 0.5
  t <- t.test(d[,columns[i]])
  points(x, t$estimate, pch = 16, cex = 1.8, col = colors[i])
  lines(c(x, x), c(t$conf.int[1], t$conf.int[2]), lwd = 5, col = colors[i], lend = 2)  
  text(x = x, y = 250, labels = sprintf("%.1f [%.1f, %.1f]", t$estimate, t$conf.int[1], t$conf.int[2]), srt = 90, adj = 0, cex = 0.6)
} 
mtext("Average", side = 1, line = 3.5, at = 2.5, cex = 2)

dev.off()

par(mfrow=c(1,1))





png("Fig4appendix.png", width = 1450, height = 2050, pointsize = 24)

preds <- c("Honesty_Humility", "Emotionality", "Extraversion", "Agreeableness",
           "Conscientiousness", "Openness_to_Experience", "risk_aversion", "prosociality", "reported",
           "highloss.c", "info.c")
pnames <- c("Honesty-Humility", "Emotionality", "Extraversion",
            "Agreeableness", "Conscientiousness", "Openness to experience", "Risk aversion", "Prosociality", "Baseline cheating",
            "High loss condition", "Information condition")
dvs<- c("bdm3", "auction4", "auction5", "auction6", "bdm7")
cols <- c("black", "red", "red", "red", "black")

par(las = 1, cex.axis = 1.35, cex.lab = 1.55, mar = c(1, 16, 6, 10))
plot(0,0,
     ylim = c(0,length(preds)), xlim = c(-0.5, 0.5),
     xlab = "", ylab = "",
     xaxs = "i", yaxs = "i",
     main = "",
     type = "n",
     xaxt = "n", yaxt = "n",
     axes = F
)
axis(side = 3, at = seq(-0.5,0.5,0.1), labels = seq(-0.5,0.5,0.1), cex.axis = 1)
abline(v = 0, lwd = 2, lty = 3)
for(i in 1:length(preds)) {
  y <- length(preds)- i + 0.5
  mtext(text = pnames[i], side = 2, line = 2.5, at = y, cex = 1.5, las = 1)
  for(j in 1:length(dvs)) {
    y <- length(preds)- i + 0.5 - (j-1)*0.15 + (length(dvs) - 1)*0.075
    sci <- spearman.ci(d[d$attention, preds[i]], d[d$attention, dvs[j]], nrep = 1000)
    points(sci$estimate, y, pch = 16, cex = 2, col = cols[j])
    lines(c(sci$conf.int[1], sci$conf.int[2]), c(y, y), lend = 2, lwd = 3, col = cols[j])  
    mtext(text = sprintf("%s [%s, %s]", shorten(sci$estimate), shorten(sci$conf.int[1]), shorten(sci$conf.int[2])), side = 4, line = 2.5, at = y, cex = 1, las = 1)
  }
}
mtext(text = "Correlation with the willingness to pay", side = 3, line = 3, at = 0, cex = 2)

dev.off()







addhist2 <- function(vec, n, group = "", maxy = 0.71) {
  plot(0,0,
       ylim = c(0, maxy), xlim = c(-0.5, n + 0.5),
       xlab = "", ylab = "",
       xaxs = "i", yaxs = "i",
       main = "", 
       type = "n",
       xaxt = "n", yaxt = "n",
       axes = F
  )  
  for(i in seq(0, maxy, 0.1)) {
    abline(h = i, lty = 3, col = "grey")
  }
  abline(v = n/2, lty = 2)
  for(i in 0:n) {
    par(xpd = TRUE)
    rect(xleft = i - 0.5, ybottom = 0, xright = i + 0.5, ytop = sum(vec == i, na.rm = T)/sum(!is.na(vec)), col = "grey")
    text(x = i, y = 0.4, labels = sum(vec == i, na.rm = T))
    par(xpd = FALSE)
    points(x = i, y = dbinom(x = i, size = n, prob = 0.5), pch = 4, cex = 0.8, lwd = 2)
  }
  axis(side = 2, at = seq(0, maxy, 0.1))
  points(x = mean(vec, na.rm = T), y = maxy - 0.04, pch = 16, cex = 2, col = "black")
  cis <- t.test(vec)$conf.int
  lines(x = cis, y = rep(maxy - 0.04, 2), lwd = 3, lend = 2, col = "black")
  text(x = cis[1] - 0.2, y = maxy - 0.04, labels = sprintf("%.2f [%.2f, %.2f]", mean(vec, na.rm = T), cis[1], cis[2]), adj = 1, cex = 0.8)
  shadowtext(x = -0.2, y = maxy - 0.07, labels = group, adj = 0, cex = 1.8, col = "black", bg = "white")
}
addCIs2 <- function(vec) {
  y <- par("usr")[4] - 0.08
  points(x = mean(vec, na.rm = T), y = y, pch = 16, cex = 2, col = "grey")
  cis <- t.test(vec)$conf.int
  lines(x = cis, y = rep(y, 2), lwd = 3, lend = 2, col = "grey")
  text(x = cis[1] - 0.2, y = y, labels = sprintf("%.2f [%.2f, %.2f]", mean(vec, na.rm = T), cis[1], cis[2]), adj = 1, cex = 0.8)
}



png("Fig2appendix.png", width = 1250, height = 1850, pointsize = 24)
par(las = 1, cex.axis = 1.5, cex.lab = 1.55, oma = c(4,3,0,0))
layout(matrix(1:9, 9, 1, byrow = TRUE), heights = c(1, rep(3,2), 1, rep(3,5)))
par(mar = c(0,0,0,0))
plot(0,0, type="n", axes = F, xlim = c(0,1), ylim = c(0,1))
text(labels = "Baseline", x = 0.5, y = 0.5, cex = 2.2)
par(mar = c(1,3,0.5,1))
addhist2(d$reported[d$highloss], 12, sprintf("High loss, n = %i", sum(d$highloss)))
addhist2(d$reported[!d$highloss], 12, sprintf("Low loss, n = %i", sum(!d$highloss)))
par(mar = c(0,0,0,0))
plot(0,0, type="n", axes = F, xlim = c(0,1), ylim = c(0,1))
text(labels = "After payment", x = 0.5, y = 0.5, cex = 2.2)
par(mar = c(1,3,0.5,1))
addhist2(d$reported3[d$after3], 12, sprintf("After BDM, 3rd block, n = %i", sum(d$after3)))
addCIs2(d$reported[d$after3])
addhist2(d$reported4[d$after4], 12, sprintf("After Auction, 4th block, n = %i", sum(d$after4, na.rm = T)))
addCIs2(d$reported[d$after4])
mtext(text = "Probability", side = 2, line = 3.7, at = 0.6, cex = 1.5, las = 3)
addhist2(d$reported5[d$after5], 12, sprintf("After Auction, 5th block, n = %i", sum(d$after5, na.rm = T)))
addCIs2(d$reported[d$after5])
addhist2(d$reported6[d$after6], 12, sprintf("After Auction, 6th block, n = %i", sum(d$after6, na.rm = T)))
addCIs2(d$reported[d$after6])
addhist2(d$reported7[d$after7], 12, sprintf("After BDM, 7th block, n = %i", sum(d$after7, na.rm = T)))
addCIs2(d$reported[d$after7])
axis(side = 1, at = 0:12)
mtext(text = "Number of reported correct predictions", side = 1, line = 3.2, at = 6, cex = 1.5)
dev.off()
