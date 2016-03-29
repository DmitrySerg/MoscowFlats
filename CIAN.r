##########################################################
##### Параметрическая и байесовская регрессия (CIAN) #####
##########################################################



library(corrplot)
library(arm)
library(MCMCpack)

#### Считываем данные, преобраозвываем в формат data.frame
flats <- read.csv("C:/Users/Auditore/Desktop/flats.csv", header=TRUE)
flats <- as.data.frame(flats)
flats$X <- NULL


#### Присваиваем пустым значениям Balcony, Telephone, Elevator, floor1 и floor2 нули
#### предполагая, что раз владельцы не указали их наличие, то их нет
flats$floor1[is.na(flats$floor1)] <- 0
flats$floor2[is.na(flats$floor2)] <- 0
flats$Bal[is.na(flats$Bal)] <- 0
flats$Tel[is.na(flats$Tel)] <- 0
flats$Elevat[is.na(flats$Elevat)] <- 0


#### Два весёлых цикла, которые присваивают пропущенным значениям жилой и кухонной площади
#### средние значения по ближайшим по общей площади квартирам
for(i in 1:length(flats$Kitsp)){
  if(is.na(flats$Kitsp[i])){
    flats$Kitsp[i] <- mean(na.omit(flats$Kitsp[flats$Totsp-10 < flats$Totsp[i] & flats$Totsp[i] < flats$Totsp[i]+10 ]))
  }
}

for(i in 1:length(flats$Livesp)){
  if(is.na(flats$Livesp[i])){
    flats$Livesp[i] <- mean(na.omit(flats$Livesp[flats$Totsp-10 < flats$Totsp[i] & flats$Totsp[i] < flats$Totsp[i]+10 ]))
  }
}


#### Убираем оставшиеся пустые значения
flats <- na.omit(flats)

#### Итого есть 6958 значений, ура!
sum(complete.cases(flats))

#### Уберём из датасета названия станций метро (они могут пригодиться для красивой визуализации)
Metro <- flats$Metro
flats$Metro <- NULL



#### Проверим коррелированность факторов
corrplot(cor(flats), method = "number", type="lower")

#### У Totsp и Livesp корреляция составила 0.92, удалим Livesp, также удалим Floor, она объясняется floor1 и floor2
flats$Livesp <- NULL
flats$Floor <- NULL

#### Снова роверим коррелированность факторов и убедимся, что всё стало миленько и красивенько
corrplot(cor(flats), method = "number", type="lower")



base_model <- lm(data=flats, Price~Brick+
                   as.factor(District)+
                   Floors+
                   Metrdist+
                   NFloor+
                   New+
                   as.factor(Rooms)+
                   Totsp+
                   Walk+
                   distance+
                   Bal+ Elevat+ Tel+
                   Kitsp+
                   floor1+
                   floor2)
summary(base_model)

shapiro.test(base_model$residuals)
jarqueberaTest(base_model$residuals)



#### Посмотрим модельку чисто по округам Москвы, базовым округом является ЦАО
#### Из модели мы видим, что цена очень сильно зависит от района и имеет смысл разбиьт выборку по ним
model_district <- lm(data=flats, Price~as.factor(District))
summary(model_district)


#### Первая модель будет по ЦАО
#### Убираем из модели расстояние до метро, расстояние до центра, Walk
flats_CAO <- flats[flats$District==0,]
flats_CAO$District <- NULL

corrplot(cor(flats_CAO), method="number")

CAO_model <- lm(data=flats_CAO, Price~Brick+
                  Floors+
                  NFloor+
                  New+
                  as.factor(Rooms)+
                  Totsp+
                  Bal+ Elevat+ Tel+
                  Kitsp+
                  floor1+
                  floor2)
summary(CAO_model)

#### Bayesian (from amr)
CAO_bayes <- bayesglm(data=flats_CAO, Price~Brick+
                  Floors+
                  NFloor+
                  New+
                  as.factor(Rooms)+
                  Totsp+
                  Bal+ Elevat+ Tel+
                  Kitsp+
                  floor1+
                  floor2,
                  prior.mean = 0,
                  prior.scale = Inf,
                  prior.df = Inf,
                  family = gaussian)

summary(CAO_bayes)
simulates <- coef(sim(CAO_bayes))

par(mfrow = c(3,7))
for(i in 1:21){
  posterior <- simulates[,i]
  hist(posterior, prob = TRUE, main = i)
  lines(density(posterior), col='blue', lwd = 2)
  lines(density(posterior, adjust=2), lty="dotted", col="darkgreen", lwd=2) 
}

par(mfrow = c(1,1))
