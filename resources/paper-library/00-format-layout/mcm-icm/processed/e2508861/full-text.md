# E2508861.pdf 可检索文本

> 本文件由原 PDF 自动提取，仅用于检索和定位；公式、表格与版式以原 PDF 或对应页图为准。

- 源文件：`../../E2508861.pdf`
- SHA-256：`3214E26E68A446B4B4B1BC84007FB0A2DE6FB32B9AF833617206CD7AB16C2984`
- 页数：27

## 第 001 页

[查看原页版式](pages/page-001.jpg)

~~~~text
 
 
Symphony of Eco-Agriculture:  
A New Music of Harmonious Coexistence 
Summary 
The global expansion of agricultural land has led to problems such as ecosystem imbal-
ance, biodiversity loss, and reduced agricultural productivity. To address these challenges, we 
developed two models: Model I, the Forest-to-Agriculture Transition Ecosystem (FATE) 
Model; Model II, the Comprehensive Organic Management and Planning (COMAP) 
Model. 
In Model I, the biggest innovation is the combination of the Lotka-Volterra model with 
a generalized Logistic model, incorporating a spatial diffusion term to describe population 
migration. We also examined the impacts of herbicides, insecticides, and fertilizers. Based 
on Assumption 1, we introduced a seasonal variation function to refine the agricultural cycle 
in the original model. Comparing ecosystem dynamics under different chemical use scenarios 
(e.g., no insecticides, no fertilizers, or all three chemicals), we found that the absence of in-
secticides led to uncontrolled pest populations and ecosystem collapse. 
Subsequently, we used Model I to explore the effects of species regression through multi-
scenario simulations combined with probability estimations, focusing on producers 
(shrubs), secondary consumers (larks), and pollinators (bees). Among these, Scenario C (larks 
and shrubs) performed best, as larks enhanced system stability through pest control, while 
shrubs supported ecological diversity and stable crop growth. 
Additionally, we analyzed two human interventions: the herbicide-reduction strategy and 
a biodiversity assessment considering bats' pollination function. Results showed that reducing 
herbicide usage improved wheat population growth and ecosystem resilience. Bats signifi-
cantly enhanced wheat productivity, achieving a system stability and resilience index of 6.42, 
compared to 5.01 for frogs. 
For Model II, our greatest highlight is to solve the multi-objective optimization problem 
by using the Convex Reformulation Method to trade-off the ecological benefits (biodiversity 
and system stability) with the economic benefits (agricultural yield and revenue). After prov-
ing the model’s concave nature, we solved it using the pairwise transformation and ε-constraint 
methods. The ecological target value reached 243.58, indicating improvements in biodiversity 
and stability, while the economic target value was 13,484.36 USD/month, demonstrating ag-
ricultural viability. The pest density weighting coefficient (0.45) emphasized its critical role, 
while the trade-off coefficient (0.57) indicated a bias toward ecological optimization. 
Finally, sensitivity analyses on Model I revealed that species mortality had a small influ-
ence on model stability, while insecticide parameters were particularly sensitive to system 
performance. Based on these findings, we propose optimizations for farmers  
 
Keywords: FATE Model; COMAP Model; Lotka-Volterra Equation; Eco-Agriculture； 
Convex Reformulation
Problem Chosen 
E 
2025 
MCM/ICM 
Summary Sheet 
Team Control Number 
2508861 
~~~~

## 第 002 页

[查看原页版式](pages/page-002.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
           Page 2 of 25 
 
Contents 
1 Introduction ...................................................................................................... 3 
1.1 Background ...................................................................................................................... 3 
1.2 Restatement of the Problem ............................................................................................. 3 
1.3 Literature Review ............................................................................................................. 4 
1.4 Our Work .......................................................................................................................... 4 
2 Assumptions and Justifications ....................................................................... 4 
3 Notations and Data Sources ............................................................................ 5 
3.1 Notations .......................................................................................................................... 5 
3.2 Data Sources .................................................................................................................... 6 
4 Model Ⅰ: Forest- to-Agriculture Transition Ecosystem ................................ 6 
4.1 Model Overview ............................................................................................................... 6 
4.2 Multi-Trophic Food Web .................................................................................................. 7 
4.2.1 Multi-Trophic Dynamic Population Modeling ....................................................... 7 
4.2.2 Agricultural Cycles and Seasonal Variations ........................................................ 10 
4.2.3 Model I Solution ................................................................................................... 11 
4.3 Results of Model I .......................................................................................................... 12 
5 Analysis of Species Return Under Multi-Scenario Simulation .................. 13 
5.1 Species Distribution Model ............................................................................................ 14 
5.1.1 Probability Calculation Method ........................................................................... 14 
5.1.2 Calculation Results and Evaluation ...................................................................... 14 
5.2 Multi-Scenario Simulations ........................................................................................... 15 
5.3 Scenario Simulation Results .......................................................................................... 15 
6 Analysis of Chemical Dependency and Biodiversity Synergy ................... 16 
6.1 Herbicide Dependency Reduction .................................................................................. 16 
6.2 Biodiversity Synergy ...................................................................................................... 17 
6.3 Calculated Results ......................................................................................................... 18 
7 Model II: Comprehensive Organic Management and Planning ............... 19 
7.1 Model Preparation ......................................................................................................... 19 
7.2 Model Construction ....................................................................................................... 19 
7.3 Calculated results .......................................................................................................... 21 
8 Sensitivity Analysis ......................................................................................... 21 
9 Strengths and Weaknesses ............................................................................. 22 
9.1 Strengths ......................................................................................................................... 22 
9.2 Weaknesses ..................................................................................................................... 22 
10 Conclusion ..................................................................................................... 23 
References .......................................................................................................... 23 
Appendices ......................................................................................................... 24 
Proof 1: Mathematical Expression of Spatial Dimensions .................................................. 24 
Proof 2: Concavity of the COMAP Model ........................................................................... 24 
 
~~~~

## 第 003 页

[查看原页版式](pages/page-003.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 3 of 25 
 
1 Introduction 
1.1 Background 
The growing global demand for agriculture has driven the large-scale conversion of for-
ests into agricultural land and the transformation of complex ecosystems into monoculture 
farming landscapes. This shift has resulted in challenges such as soil degradation and pest out-
breaks, compelling farmers to rely heavily on chemicals (e.g., insecticides and herbicides) to 
maintain crop yields. However, prolonged chemical use disrupts ecological balance, diminishes 
native species diversity, and undermines agroecosystem sustainability [1]. To address these 
challenges, the introduction of beneficial insects (e.g., bats and bees) has been shown to restore 
ecological balance, improve crop productivity, and enhance soil health [2]. Balancing agricul-
tural development with ecological conservation remains a critical global concern. Accordingly, 
we utilize ecosystem dynamic modeling and decision-making simulations (Figure 1) to pro-
vide scientific insights for policy formulation and promote the sustainable development of eco-
friendly agriculture. 
 
Figure 1: Conversion of Forest Ecology to Agroecology 
1.2 Restatement of the Problem 
Given the above context, we aim to analyze ecosystem dynamics and their interactions 
with anthropogenic decisions following the conversion of forests into agricultural land by con-
structing a mathematical model. Our study focuses on the following aspects: 
 Natural Process Analysis: Develop an ecosystem dynamic model to capture ecological 
changes after forest conversion into agricultural land. This includes establishing the 
food web structure, evaluating the impacts of agricultural cycles and chemical use on 
plant and consumer populations, and assessing the role of species reintroduction in eco-
logical restoration within marginal habitats (Tasks I & II). 
 Anthropogenic Decision-Making Assessment: Investigate the effects of various agri-
cultural management decisions on ecosystems, including the role of chemical reduction 
and the introduction of key species (e.g., bats and bees) in pest control and system sta-
bility. Additionally, simulate the combined impacts of green agricultural practices on 
ecosystem services, crop productivity, and economic benefits (Tasks III & IV). 
 Policy Recommendation Development: Based on the modeling results, propose eco-
friendly agricultural strategies that balance economic viability and ecological sustaina-
~~~~

## 第 004 页

[查看原页版式](pages/page-004.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 4 of 25 
 
bility. Furthermore, explore the potential of policy incentives to promote green agricul-
tural practices (Task V). 
1.3 Literature Review 
Forest ecosystems feature complex food chains and high species diversity, with soil health 
relying on natural cycles [3]. Interactions among plants, herbivores, carnivores, and decompos-
ers are vital for maintaining balance. In contrast, agroecosystems, dominated by monocrops 
with low biodiversity, are further disrupted by fertilizers and insecticides [4]. 
Agricultural transformation is influenced by natural evolution and human activities. Herb-
icides and insecticides affect crop health and pest dynamics, while species like bats support 
recovery through pest control and pollination. Similarly, bird reintroduction aids in restoring 
ecological balance [5]. Organic agriculture provides a sustainable alternative by reducing 
chemical inputs and enhancing soil health and diversity, though short-term challenges in yield 
and cost remain. 
Common ecological and food web models include the Logistic model, Lotka-Volterra 
model, and food web model, with their respective strengths and limitations shown in Figure 2. 
 
Figure 2: Literature Review Chart 
1.4 Our Work 
To address this issue, our working framework is shown in Figure 3. 
2 Assumptions and Justifications 
In order to simplify the problem and improve the model's tractability and computational 
efficiency, we make the following assumptions: 
Assumption 1: Crops are predominantly seasonal, and the agricultural cycle aligns with 
seasonal variations. 
Justification: This assumption is based on the growth characteristics of seasonal crops, 
where major agricultural activities in agroecosystems (e.g., sowing, growing, fertilizing, har-
vesting) are driven by seasonal climatic conditions. By aligning the agricultural cycle with 
seasonal variations, the model is simplified, allowing the use of a uniform periodic function to 
describe both agricultural cycles and seasonal changes, thereby enhancing the rationality of 
dynamic modeling. 
Assumption 2: Herbicides are primarily used during the early stages of agroecosystems 
to control weed expansion. 
~~~~

## 第 005 页

[查看原页版式](pages/page-005.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 5 of 25 
 
Justification: During the transition from forests to agroecosystems, legacy weeds quickly 
adapt and compete for farmland resources. To ensure optimal crop growth and reduce compe-
tition from weeds, farmers commonly use herbicides to manage agricultural systems during 
their establishment phase. This reflects a widely observed pattern in agricultural practices. 
Assumption 3: The actual study area has a spherical quadrilateral distribution but is sim-
plified to a planar rectangular projection in the model. This simplification does not significantly 
affect the accuracy of the model results. 
Justification: Given the relatively small size of the study area, the impact of latitude and 
longitude changes on spherical distances can be precisely calculated using the Haversine for-
mula. Simplifying the sphere to a planar rectangular projection reduces model complexity 
while maintaining sufficient geographic accuracy. This ensures the scientific validity of model 
analyses and results. 
Assumption 4: It is assumed that all data collected are reliable. 
Justification: This assumption ensures the accuracy of the data input to the model and 
avoids analytical bias due to data errors, thus allowing the study to focus more on the model 
mechanism itself. 
 
Figure 3: Our Work Framework Diagram 
3 Notations and Data Sources 
3.1 Notations 
The primary notations used in this paper are listed in Table 1. 
~~~~

## 第 006 页

[查看原页版式](pages/page-006.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 6 of 25 
 
Table 1: Notations used in this paper 
Symbol 
Description 
Unit 
For 
Model I 
𝐷𝐷 
Spatial diffusion coefficient 
km²/mouth 
𝐶𝐶ℎ
𝑖𝑖 
Concentration of class i chemicals 
mg/L 
𝑃𝑃 
Total population density of primary producers 
Individuals/km2 
For 
Model II 
𝐵𝐵(𝑡𝑡) 
Biodiversity index 
N/A 
𝑃𝑃𝑝𝑝𝑝𝑝𝑝𝑝𝑝𝑝(𝑡𝑡) 
Indicates pest density 
Individuals/km2 
𝑅𝑅𝑚𝑚𝑚𝑚𝑚𝑚𝑚𝑚𝑚𝑚𝑚𝑚(𝑡𝑡) Indicates market yield 
USD/mouth 
*There are some variables that are not listed here and will be discussed in detail in each section. 
3.2 Data Sources 
The “Corn Belt” in the Midwestern U.S. is one of the most important agricultural regions 
in North America, known for its high-yielding crops (e.g., corn and soybeans) and typical agro-
ecosystems, making it a suitable study area. We collected data related to crop populations [6], 
biodiversity [7], climate [7], and soils [8] within the region. 
Since the geographic extent of the region lies roughly between 37𝑜𝑜𝑁𝑁 to 48𝑜𝑜𝑁𝑁 and 
90𝑜𝑜𝑁𝑁 to 100𝑜𝑜𝑁𝑁, to simplify the study, although the actual study area is distributed in a spher-
ical quadrilateral (Figure 4), according to Assumption 3 we projected the region into a planar 
rectangular coordinate system for processing. In the model, the shortest spherical distance be-
tween two points expressed in latitude and longitude are converted using Haversine's formula, 
which is shown below: 
𝑑𝑑= 2𝑟𝑟∗𝑎𝑎𝑎𝑎𝑎𝑎𝑎𝑎𝑎𝑎𝑛𝑛ቌඨ𝑠𝑠𝑠𝑠𝑠𝑠2 ൬𝛥𝛥𝛥𝛥
2 ൰+ cos(𝜙𝜙1) cos(𝜙𝜙2) 𝑠𝑠𝑠𝑠𝑠𝑠2 ൬𝛥𝛥𝛥𝛥
2 ൰ቍ, 
( 1 )  
here, 𝑟𝑟 represents the Earth's radius, 𝜙𝜙1 and 𝜙𝜙2 denote the latitudes of two points, and Δ𝜙𝜙 
and Δ𝜆𝜆 represent the differences in latitude and longitude, respectively. This formula serves 
as the standard method for calculating spherical distances, ensuring the spatial accuracy of the 
model. 
 
Figure 4: Abstracting a Quadrilateral into a Rectangle 
4 Model Ⅰ: Forest- to-Agriculture Transition Ecosystem 
4.1 Model Overview 
To model the current ecosystem and analyze the dynamics of the forest-to-agriculture 
transition, we developed the Forest-to-Agriculture Transition Ecosystem (FATE) Model. 
The model's key innovation lies in incorporating spatial dimensions and environ-
mental factors, capturing population diffusion and the dynamic effects of variables such as 
temperature and chemical concentrations on the ecosystem. 
We mathematically defined the spatial dimension and constructed a multi-trophic food 
~~~~

## 第 007 页

[查看原页版式](pages/page-007.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 7 of 25 
 
web by integrating the Lotka-Volterra and generalized Logistic models to describe energy 
flows among producers, consumers, and decomposers. Agricultural cycles, seasonal variations, 
and environmental variables were then incorporated to quantify, from a spatiotemporal per-
spective, the combined effects of agricultural activities and chemical use on population dynam-
ics and ecosystem stability. 
4.2 Multi-Trophic Food Web 
The multi-trophic food web we constructed includes primary producers, primary con-
sumers, secondary consumers, tertiary consumers, and decomposers, while incorporating 
the dynamic effects of herbicides, insecticides, and fertilizers. Primary producers form the 
foundation, supplying energy that flows upward through trophic levels, while decomposers 
recycle nutrients by breaking down organic matter. Predation and energy transfer govern the 
interactions between these levels, maintaining ecological balance. Figure 5 provides a sche-
matic representation of these relationships. 
 
Figure 5: Map of Food Web Relationships 
Definition 1: Mathematical Expression of Spatial Dimension. In ecosystem modeling, the 
spatial dimension can be described using a spatial diffusion term, which characterizes the mi-
 
Specifically, for the population density 𝑃𝑃(𝑥𝑥, 𝑡𝑡) 
gration and distribution behavior of populations in space [9].
of a species, its diffusion behavior in the 
spatial dimension can be expressed as: 
∂𝑃𝑃(𝑥𝑥, 𝑡𝑡)
∂𝑡𝑡
= 𝐷𝐷∇2𝑃𝑃(𝑥𝑥, 𝑡𝑡), 
( 2 )  
Where, 𝑃𝑃(𝑥𝑥, 𝑡𝑡) denotes the population density at location 𝑥𝑥 and time 𝑡𝑡, 𝐷𝐷 represents the 
diffusion coefficient reflecting the rate of population diffusion in space, and ∇2𝑃𝑃(𝑥𝑥, 𝑡𝑡) is the 
Laplace operator, defined as: 
∇2𝑃𝑃= ∂2𝑃𝑃
∂𝑥𝑥2 + ∂2𝑃𝑃
∂𝑦𝑦2  (in two dimensions) , 
( 3 )  
which represents the spatial gradient of changes in population density. The physical interpreta-
tion of this diffusion term is that the temporal change in population density is determined by 
the spatial non-uniformity of its distribution. The full derivation of this formula is provided in 
Appendix Proof 1. 
4.2.1 Multi-Trophic Dynamic Population Modeling 
To comprehensively characterize the dynamic changes and ecological effects of chemical 
agents during the transition from forest ecosystems to agricultural ecosystems, we introduced 
three types of chemicals: herbicides, insecticides, and fertilizers. These are applied to suppress 
~~~~

## 第 008 页

[查看原页版式](pages/page-008.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 8 of 25 
 
weeds, reduce pests, and enhance soil nutrients, respectively. The dynamics of these chemicals 
are modeled using partial differential equations, expressed as follows: 
∂𝐶𝐶ℎ
𝑖𝑖
∂𝑡𝑡= 𝐷𝐷ℎ
𝑖𝑖∇2𝐶𝐶ℎ
𝑖𝑖+ 𝑅𝑅𝑖𝑖(𝑥𝑥, 𝑡𝑡) −𝛼𝛼𝑖𝑖𝐶𝐶ℎ
𝑖𝑖, (𝑖𝑖= her, ins, fer ), 
( 4 )  
where, 𝐶𝐶ℎ
𝑖𝑖 denotes the concentration of the 𝑖𝑖-th chemical agent; 𝐷𝐷ℎ
𝑖𝑖 represents the diffusion 
coefficient of the 𝑖𝑖-th chemical, indicating its spatial distribution and diffusion; 𝑅𝑅𝑖𝑖(𝑥𝑥, 𝑡𝑡) de-
notes the application rate of the 𝑖𝑖-th chemical, which depends on the agricultural cycle and is 
defined as: 
𝑅𝑅𝑖𝑖(𝑥𝑥, 𝑡𝑡) = ൜𝑟𝑟𝑖𝑖,
𝑡𝑡∈𝑇𝑇1
0,
𝑡𝑡∈𝑇𝑇2, 
( 5 )  
here, 𝑇𝑇1 and 𝑇𝑇2 represent the application phase and non-application phase of the agricultural 
cycle, respectively. 𝛼𝛼𝑖𝑖 denotes the degradation rate of the 𝑖𝑖-th chemical agent. 
The ecological impacts of these chemicals on various trophic levels of the ecosystem are 
illustrated in Figure 66. 
 
Figure 6: Role of Chemicals in Food Webs 
 Ecological Impacts of Herbicides: Herbicides positively impact crop growth by sup-
pressing weed population densities, thereby indirectly increasing available survival re-
sources for crops. However, the reduction in weed residues diminishes decomposer 
activity and disrupts soil nutrient cycling. 
 Ecological Impacts of Insecticides: Insecticides effectively reduce pest densities and pre-
dation pressure on crops. However, they may also exhibit toxicity to secondary consumers 
such as ladybug beetles, indirectly weakening pest control. Additionally, insecticide res-
idues can harm decomposers, lowering decomposition efficiency and compromising 
soil stability. 
 Ecological Impacts of Fertilizers: Fertilizers directly enhance crop growth and competi-
tiveness by enriching soil nutrients. However, overuse can disrupt the chemical balance 
of the soil, inhibit decomposer activity, reduce microbial diversity, and ultimately affect 
overall ecosystem health. 
Based on the multi-trophic structure of the ecosystem and the multifaceted impacts of 
chemical dynamics, we formulated population dynamics equations for each trophic level. The 
detailed equations are as follows. 
Primary Producers (Wheats and Weeds) 
Primary producers include wheats (crops) and weeds, whose growth is influenced by dy-
namic changes in environmental carrying capacity, predation pressure from primary consumers, 
and the combined effects of chemical agents. The governing equation is as follows: 
~~~~

## 第 009 页

[查看原页版式](pages/page-009.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 9 of 25 
 
𝜕𝜕𝜕𝜕
𝜕𝜕𝜕𝜕= 𝐷𝐷𝑃𝑃𝛻𝛻2𝑃𝑃+ 𝑟𝑟𝑃𝑃𝑃𝑃൬1 −
𝑃𝑃
𝐾𝐾(𝑥𝑥, 𝑡𝑡)൰−𝑎𝑎1𝑃𝑃𝐶𝐶1 −𝛽𝛽1𝐶𝐶ℎ
her 𝑃𝑃weeds + 𝜆𝜆𝐶𝐶ℎ
𝑓𝑓𝑓𝑓𝑓𝑓𝑃𝑃wheats −𝑑𝑑𝑃𝑃𝑃𝑃, ( 6 )  
where, 𝑃𝑃 denotes the total population density of primary producers, including wheats and 
weeds. 𝑟𝑟𝑃𝑃 represents the intrinsic growth rate, indicating the maximum growth rate of primary 
producers under unlimited resource conditions. 𝑎𝑎1 denotes the predation efficiency of primary 
consumers, and 𝐶𝐶1 represents the total population density of primary consumers. 𝑃𝑃weeds  and 
𝑃𝑃wheats  denote the population densities of weeds and wheats, respectively. 𝑑𝑑𝑃𝑃 is the natural 
mortality coefficient of primary producers. The term  
൬1 −
𝑃𝑃
𝐾𝐾(𝑥𝑥, 𝑡𝑡)൰, 
( 7 )  
is the generalized Logistic growth limitation, which constrains population growth according to 
the environmental carrying capacity. When 𝑃𝑃< 𝐾𝐾(𝑥𝑥, 𝑡𝑡) , the population grows; as 𝑃𝑃→
𝐾𝐾(𝑥𝑥, 𝑡𝑡), growth approaches zero. The dynamic environmental carrying capacity 𝐾𝐾(𝑥𝑥, 𝑡𝑡) is de-
fined as follows: 
𝐾𝐾(𝑥𝑥, 𝑡𝑡) = 𝐾𝐾0 + 𝜙𝜙𝐷𝐷𝐷𝐷+ 𝜆𝜆𝐶𝐶ℎ
𝑓𝑓𝑓𝑓𝑓𝑓−𝛽𝛽1𝐶𝐶ℎ
ℎ𝑒𝑒𝑒𝑒−𝛽𝛽2𝐶𝐶ℎ
𝑖𝑖𝑖𝑖𝑖𝑖, 
( 8 )  
where, 𝐾𝐾0 represents the baseline environmental carrying capacity of primary producers. 𝜙𝜙𝐷𝐷 
indicates the positive contribution of decomposers ( 𝐷𝐷 ) to soil nutrients. 𝜆𝜆𝐶𝐶ℎ
fer, 𝛽𝛽1𝐶𝐶ℎ
ℎ𝑒𝑒𝑒𝑒, and 
𝛽𝛽2𝐶𝐶ℎ
ins  represent the effects of fertilizers, herbicides, and insecticides, respectively, on the car-
rying capacity. 
Primary Consumers (Aphids and Field Mice) 
The population dynamics of primary consumers, including aphids and field mice, are pri-
marily driven by the supply of primary producers, while being influenced by predation from 
secondary consumers and the direct toxic effects of insecticides. The governing equation is as 
follows: 
𝜕𝜕𝐶𝐶1
𝜕𝜕𝜕𝜕= 𝐷𝐷𝐶𝐶1𝛻𝛻2𝐶𝐶1 + 𝑟𝑟𝐶𝐶1,0
𝑃𝑃
𝑃𝑃+ ℎ𝑃𝑃
𝐶𝐶1 −𝑎𝑎2𝐶𝐶1𝐶𝐶2 −𝛾𝛾𝐶𝐶ℎ
𝑖𝑖𝑖𝑖𝑖𝑖𝐶𝐶1 −𝑑𝑑𝐶𝐶1𝐶𝐶1, 
( 9 )  
where, 𝑟𝑟𝐶𝐶1,0 represents the support rate provided by primary producers to primary consumers. 
ℎ𝑃𝑃 denotes the saturation constant for predation at the primary trophic level. 𝑎𝑎2 indicates the 
predation effect of secondary consumers. 𝛾𝛾 represents the toxicity rate of insecticides (𝐶𝐶ℎ
ins ) 
on primary consumers. 𝑑𝑑𝐶𝐶1 is the natural mortality coefficient of primary consumers. 
This equation captures the balance between resource availability from primary producers, 
predation pressure from secondary consumers, and the detrimental effects of insecticides on 
primary consumer populations. 
Secondary Consumers (Ladybugs and Bats) 
Secondary consumers, including ladybugs and bats, are influenced by their efficiency in 
preying on primary consumers, predation pressure from tertiary consumers, and population 
decline caused by the non-target effects of insecticides. The governing equation is as follows: 
∂𝐶𝐶2
∂𝑡𝑡= 𝐷𝐷𝐶𝐶2∇2𝐶𝐶2 + 𝑏𝑏1
𝐶𝐶1
𝐶𝐶1 + ℎ𝐶𝐶1
𝐶𝐶2 −𝑎𝑎3𝐶𝐶2𝐶𝐶3 −𝛾𝛾𝐶𝐶ℎ
ins𝐶𝐶2
lad −𝑑𝑑𝐶𝐶2𝐶𝐶2, 
( 10 ) 
where, 𝐶𝐶2 represents the total population density of secondary consumers. 𝑏𝑏1 denotes the 
support rate provided by primary consumers to secondary consumers. 𝑎𝑎3 indicates the preda-
tion effect of tertiary consumers. 𝛾𝛾 represents the non-target toxicity rate of insecticides 
~~~~

## 第 010 页

[查看原页版式](pages/page-010.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 10 of 25 
 
( 𝐶𝐶ℎ
ins  ) on 𝐶𝐶2
lad  (the ladybug population). 𝑑𝑑𝐶𝐶2 is the natural mortality coefficient of second-
ary consumers. 
This equation reflects the complex dynamics of secondary consumers, balancing the pos-
itive effects of prey availability and the negative effects of predation pressure and insecticide 
toxicity. 
Tertiary Consumers (Eagles and Owls) 
The population dynamics of tertiary consumers, including eagles and owls, are determined 
by the availability of secondary consumers as prey and natural mortality rates. The governing 
equation is as follows: 
∂𝐶𝐶3
∂𝑡𝑡= 𝐷𝐷𝐶𝐶3∇2𝐶𝐶3 + 𝑏𝑏2
𝐶𝐶2
𝐶𝐶2 + ℎ𝐶𝐶2
𝐶𝐶3 −𝑑𝑑𝐶𝐶3𝐶𝐶3, 
( 11 ) 
where, 𝐶𝐶3 represents the total population density of tertiary consumers. 𝑏𝑏2 denotes the sup-
port rate provided by secondary consumers to tertiary consumers. 𝑑𝑑𝐶𝐶3 is the natural mortality 
coefficient of tertiary consumers. 
Decomposers (Earthworms, Fungi, and Bacteria) 
The population dynamics of decomposers, including earthworms, fungi, and bacteria, are 
primarily influenced by the organic matter supplied by other trophic levels and the positive and 
negative effects of chemical agents. The governing equation is as follows: 
∂𝐷𝐷
∂𝑡𝑡= 𝑟𝑟𝐷𝐷𝐷𝐷+ ෍ 
4
𝑖𝑖=1
𝑑𝑑𝐶𝐶𝑖𝑖𝐶𝐶𝑖𝑖−𝛿𝛿1𝐶𝐶ℎ
fer𝐷𝐷−𝛿𝛿2𝐶𝐶ℎ
her𝐷𝐷−𝛿𝛿3𝐶𝐶ℎ
ins𝐷𝐷−𝑑𝑑𝐷𝐷𝐷𝐷, 
( 12 ) 
where, ∑𝑖𝑖=1
4
 𝑑𝑑𝐶𝐶𝑖𝑖𝐶𝐶𝑖𝑖 represents the contributions of deceased individuals from all trophic levels 
to decomposers. 𝛿𝛿𝑖𝑖 denotes the toxic inhibitory effects of fertilizers ( 𝐶𝐶ℎ
fer ), herbicides 
( 𝐶𝐶ℎ
her ), and insecticides ( 𝐶𝐶ℎ
ins  ) on decomposers. 𝑑𝑑𝐷𝐷 is the natural mortality coefficient of 
decomposers. 
In summary, the FATE model integrates these equations to simulate the coupled dynamics 
of multi-trophic populations and their interactions with environmental factors and chemical 
agents. The system of equations developed for the FATE model is illustrated in Figure 7. 
 
Figure 7: Conversion of Bioenergy in Ecosystems 
4.2.2 Agricultural Cycles and Seasonal Variations 
Based on Assumption 1, which states that the agricultural cycle aligns with seasonal 
variations, we combined the dynamic characteristics of agricultural activities with sea-
~~~~

## 第 011 页

[查看原页版式](pages/page-011.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 11 of 25 
 
sonal climatic changes. These are uniformly described using a periodic function. Conse-
quently, our agricultural cycle function captures not only the changes across key phases such 
as sowing, growing, fertilizing, and harvesting but also the ecosystem's response to seasonal 
disturbances. The function is expressed as follows: 
𝑔𝑔agri(𝑡𝑡) = 𝐴𝐴1 sin ൬2𝜋𝜋𝜋𝜋
𝑇𝑇൰+ 𝐴𝐴2 cos ൬4𝜋𝜋𝜋𝜋
𝑇𝑇+ 𝜙𝜙൰+ 𝐵𝐵, 
( 13 ) 
where, 𝑇𝑇 represents the total duration of the agricultural cycle. 𝐴𝐴1 denotes the intensity of 
primary agricultural activities (first harmonic). 𝐴𝐴2 accounts for more refined characteristics 
of agricultural phases (second harmonic). 𝜙𝜙 represents the time shift of the second harmonic 
relative to the first harmonic. 𝐵𝐵 ensures the non-negativity of the function, maintaining the 
intensity of agricultural activities at positive values at all times. 
Using this function, the modified dynamics of primary producer populations and 
chemical application rates are expressed as: 
𝑔𝑔agri(𝑡𝑡)𝑅𝑅𝑖𝑖(𝑥𝑥, 𝑡𝑡), 𝑟𝑟𝑃𝑃𝑔𝑔agri(𝑡𝑡)𝑃𝑃൬1 −
𝑃𝑃
𝐾𝐾(𝑥𝑥, 𝑡𝑡)൰. 
( 14 ) 
4.2.3 Model I Solution 
During the modeling process, multiple unknown parameters were present in the model. 
By collecting ecological data from agricultural regions in North America, including crop yields, 
chemical usage, species distribution, and environmental carrying capacity, these data were used 
as prior inputs. Combined with statistical analysis, the model parameters were estimated. The 
key parameters of the model are shown in Table 2. 
Table 2: Parameter Settings 
Parameter  
Description 
Value 
Unit 
𝑟𝑟𝑃𝑃 
Growth rate of primary producers 
0.05 
1/month 
𝐾𝐾0 
Baseline environmental carrying capacity 
1000 
Individuals/km2 
𝜙𝜙𝐷𝐷 
Contribution of decomposers to carrying capacity 
20 
Individuals/km2 
𝛿𝛿1 
Negative effect of fertilizers on carrying capacity 
0.02 
1/(kg*month) 
𝛿𝛿2 
Negative effect of herbicides on weeds 
0.05 
1/(kg*month) 
𝛿𝛿2 
Negative effect of insecticides on primary consumers 0.03 
1/(kg*month) 
To solve the partial differential equations in the model, we employed the Finite Volume 
Method (FVM), a commonly used numerical approach for solving systems of partial differen-
tial equations. This method discretizes the computational domain and performs numerical in-
tegration within each control volume, thereby transforming the continuous PDE problem into 
a discrete algebraic one. 
We divided the ecosystem space into a 6 × 6 grid of subregions, with spatial step sizes 
of Δ𝑥𝑥= Δ𝑦𝑦= 1 km and time steps of Δ𝑡𝑡= 1 month. By running the simulation program, 
we obtained the distribution of primary consumers at 𝑡𝑡= 0, 𝑡𝑡= 12, 𝑡𝑡= 60 , and 𝑡𝑡= 96 
(Figure 8). 
The simulation results demonstrate the dynamic distribution of primary producers (wheats 
and weeds) at different stages and the ecological effects of chemical use: 
 Initial Stage (t=0): During the early phase of forest-to-farmland conversion, weeds domi-
nate while the wheat population is low. With no chemical application, the ecosystem reflects 
its natural state, characterized by weak competitiveness and population distribution shaped 
by natural ecological processes. 
 Crop Growth (t=12): After cultivation and moderate chemical use, the wheat population 
~~~~

## 第 012 页

[查看原页版式](pages/page-012.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 12 of 25 
 
grows significantly while weeds decline. Fertilizers enhance wheat competitiveness, and 
herbicides effectively control weed spread. 
 Moderate Use Stage (t=60): With sustained moderate chemical use, the wheat population 
stabilizes at a high level, and weeds remain suppressed. The ecosystem achieves a dynamic 
balance between decomposers and soil nutrients, supporting long-term development. 
 Overuse Stage (t=96): Excessive chemical application disrupts ecosystem balance, reducing 
decomposer activity and negatively affecting soil nutrient cycling. While wheat populations 
remain high, ecosystem stability is threatened, and weed populations are nearly eradicated. 
 
Figure 8: PDE Solving Results and Related Explanations 
4.3 Results of Model I 
To further investigate the impact of chemical agents on the population dynamics of various 
species in agroecosystems, we simulated three scenarios: no insecticide use, no fertilizer use, 
and the combined use of all three chemicals. (Based on Assumption 2, herbicides are required 
to control weed expansion caused by forest-to-farmland conversion to ensure a suitable growth 
environment for crops.) The effects of these scenarios on the temporal dynamics of all species 
in the food web were analyzed (Figures 9–11). 
       
 
Figure 9: Full chemical usage. Changes in consumer populations (left); changes in crop 
populations (right). 
~~~~

## 第 013 页

[查看原页版式](pages/page-013.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 13 of 25 
 
      
 
Figure 10: No fertilizer usage. Changes in consumer populations (left); changes in crop 
populations (right). 
      
 
Figure 11: No insecticide usage. Changes in consumer populations (left); changes in crop 
populations (right). 
Impact of Chemical Use on Consumer and Weed Populations 
 Under the scenario of full chemical use, primary consumers (aphids and field mice) and 
secondary consumers (ladybugs and bats) are significantly affected, while tertiary con-
sumers (eagles and owls) maintain relatively stable population dynamics. 
 When fertilizers are not used, crop growth is limited, leading to fluctuations at low levels 
for primary consumers, which subsequently impacts secondary and tertiary consumers, 
resulting in a lower dynamic equilibrium across these trophic levels. 
 When insecticides are not used, pests completely consume the producers, preventing their 
population growth and causing the entire ecosystem to collapse. 
Impact of Chemical Use on Crop Populations 
 In the full chemical use scenario, crop populations exhibit steady growth and reach a high 
dynamic equilibrium level. 
 Without fertilizers, due to insufficient soil nutrients, crop populations decline in the early 
stages and stabilize at a low level. 
 In the absence of insecticides, the increase in pest populations exerts a significant negative 
impact on crops, leading to a rapid decline in crop populations. 
Overall, the reasonable application of chemical agents plays a crucial role in maintaining 
the stability of crop populations and the broader ecosystem. 
5 Analysis of Species Return Under Multi-Scenario Simulation 
To analyze the impact of species reintroduction on the current agroecosystem, we used a 
species distribution model to calculate the probabilities of pollinators (bees), secondary con-
sumers (larks), and producers (shrubs) returning in different years. Based on the FATE model, 
~~~~

## 第 014 页

[查看原页版式](pages/page-014.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 14 of 25 
 
we further conducted multi-scenario simulations to dynamically analyze the ecological ef-
fects of pairwise species reintroduction combinations, quantifying their combined impacts on 
ecosystem stability, species diversity, and crop yield. 
5.1 Species Distribution Model 
The species distribution model is a tool used to predict species reintroduction probabilities 
based on environmental variables. It quantifies the influence of environmental factors on spe-
cies distribution and provides dynamic predictions. 
5.1.1 Probability Calculation Method 
Generalized Linear Models (GLM) or Generalized Additive Models (GAM) are com-
monly used to describe the relationship between reintroduction probability and environmental 
variables. The model is expressed as follows: 
𝑃𝑃( return ) = 𝑙𝑙𝑙𝑙𝑙𝑙𝑙𝑙𝑙𝑙−1 ൭𝛽𝛽0 + ෍ 
𝑛𝑛
𝑖𝑖=1
 𝛽𝛽𝑖𝑖𝑋𝑋𝑖𝑖൱ 
Where 𝑃𝑃 (return) represents the probability of a species reintroducing in a given year. logit−1 
is the inverse function of the logistic regression. 𝛽𝛽0 is the intercept term. 𝛽𝛽𝑖𝑖 denotes the re-
gression coefficient for the environmental variable 𝑋𝑋𝑖𝑖. 𝑋𝑋𝑖𝑖 represents environmental variables, 
which include: 𝑋𝑋1 : Habitat maturity. 𝑋𝑋2 : Climate conditions. 𝑋𝑋3 : Intensity of chemical 
usage. 𝑋𝑋4 : Intensity of agricultural activities. 𝑋𝑋5 : Time. 
5.1.2 Calculation Results and Evaluation 
Using the Species Distribution Model (SDM), we simulated and calculated the annual 
reintroduction probabilities of bees, larks, and shrubs over the next 10 years, along with an 
analysis of the model's performance metrics, as illustrated in Figure 12. 
 
Figure 12: Predicted Results and Model Evaluations 
The figure illustrates the reintroduction probabilities of three species (Shrub, Lark, Bee) 
over 10 years, along with the model's comprehensive evaluation. The line chart shows dynamic 
changes in reintroduction probabilities, with bees maintaining relatively stable and high prob-
abilities, while shrubs and larks exhibit greater fluctuations, reflecting their higher sensitivity 
to environmental factors and spatiotemporal conditions. 
The model evaluation results indicate high predictive accuracy for all three species (as-
sessment scores above 0.78), with bees performing slightly better than shrubs and larks. This 
confirms the model's reliability in predicting species reintroduction and underscores the vary-
ing sensitivity of species to environmental variables. These findings offer valuable insights for 
ecological conservation and restoration management. 
~~~~

## 第 015 页

[查看原页版式](pages/page-015.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 15 of 25 
 
5.2 Multi-Scenario Simulations 
To analyze the impact of species reintroduction on the current ecosystem, we conducted 
pairwise scenario analyses involving bees, larks, and shrubs. The focus was on exploring inter-
actions between species and their effects on ecosystem dynamics. 
Scenario A: Bees (Pollinators) and Shrubs (Producers) 
Scenario A: Bees and Shrubs. The dynamics of shrubs and bees are modeled by incorpo-
rating the positive feedback of pollination and resource availability: 
𝜕𝜕𝑃𝑃shrub 
𝜕𝜕𝜕𝜕
= 𝐷𝐷shrub 𝛻𝛻2𝑃𝑃shrub + 𝑟𝑟shrub 𝑃𝑃shrub ൬1 −𝑃𝑃shrub 
𝐾𝐾
൰+ 𝛾𝛾𝑏𝑏𝐵𝐵bee 𝑃𝑃shrub −𝑎𝑎1𝑃𝑃shrub (𝐶𝐶1 + 𝐶𝐶2),
𝜕𝜕𝐵𝐵bee 
𝜕𝜕𝜕𝜕
= 𝐷𝐷bee 𝛻𝛻2𝐵𝐵bee + 𝑟𝑟bee 𝐵𝐵bee ൬1 −𝐵𝐵bee 
𝐾𝐾൰+ 𝜆𝜆shrub 𝑃𝑃shrub 𝐵𝐵bee −𝛿𝛿bee 𝐵𝐵bee .
 
( 15 ) 
Scenario B: Larks (Secondary Consumers) and Bees (Pollinators) 
Scenario B: Bees and Larks. This scenario introduces the indirect reduction of pest density 
by larks in the growth function of bees, and the enhancement of food chain resources by bees 
in the growth function of larks: 
𝜕𝜕𝐵𝐵bee 
𝜕𝜕𝜕𝜕
= 𝐷𝐷bee 𝛻𝛻2𝐵𝐵bee + 𝑟𝑟bee 𝐵𝐵bee ൬1 −𝐵𝐵bee 
𝐾𝐾൰+ 𝛼𝛼lark 𝐶𝐶lark 𝐵𝐵bee −𝛿𝛿bee 𝐵𝐵bee ,
𝜕𝜕𝐶𝐶lark 
𝜕𝜕𝜕𝜕
= 𝑟𝑟lark 𝐶𝐶lark ൬1 −𝐶𝐶lark 
𝐾𝐾൰+ 𝛽𝛽bee 𝐵𝐵bee 𝐶𝐶lark −𝛿𝛿lark 𝐶𝐶lark .
 
( 16 ) 
Scenario C: Larks (Secondary Consumers) and Shrubs (Producers) 
Scenario C: Larks and Shrubs. The positive effect of larks reducing pest density is incor-
porated into the growth function of shrubs, while the habitat contribution of shrubs is added to 
the growth function of larks: 
𝜕𝜕𝑃𝑃shrub 
𝜕𝜕𝜕𝜕
= 𝐷𝐷shrub 𝛻𝛻2𝑃𝑃shrub + 𝑟𝑟shrub 𝑃𝑃shrub ൬1 −𝑃𝑃shrub 
𝐾𝐾
൰+ 𝛾𝛾𝑙𝑙𝐶𝐶lark 𝑃𝑃shrub −𝑎𝑎1𝑃𝑃shrub (𝐶𝐶1 + 𝐶𝐶2),
𝜕𝜕𝐶𝐶lark 
𝜕𝜕𝜕𝜕
= 𝑟𝑟lark 𝐶𝐶lark ൬1 −𝐶𝐶lark 
𝐾𝐾൰+ 𝜆𝜆shrub 𝑃𝑃shrub 𝐶𝐶lark −𝛿𝛿lark 𝐶𝐶lark .
 
( 17 ) 
5.3 Scenario Simulation Results 
Modeling and analysis of species reintroduction under different scenarios revealed that 
after introducing new species at t=24, ecological dynamics gradually stabilized (Figure 13), 
highlighting the regulatory role of reintroduced species. At t=84, crop populations exhibited 
exponential growth, demonstrating the long-term positive effects of species reintroduction on 
system stability and productivity. 
 Scenario A (Bees and Shrubs): Bee pollination had minimal impact on crop growth, as 
competition between shrubs and crops for resources limited population growth, making 
this the weakest scenario. 
 Scenario B (Larks and Bees): The synergy of larks and bees boosted crop growth during 
exponential phases, but initial system instability and fluctuations were observed. 
 Scenario C (Larks and Shrubs): Larks controlled pests, and shrubs supported ecological 
diversity, enabling steady crop growth and making this the most optimal scenario for long-
term stability. 
~~~~

## 第 016 页

[查看原页版式](pages/page-016.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 16 of 25 
 
 
Figure 13: Crop Dynamics Under Different Scenarios 
Under different scenarios, the dynamic effects of species reintroduction on native species 
are shown in Figures 14–16. The model results indicate that the introduction of reintroduced 
species significantly disrupted and regulated the population dynamics of native consumers. 
 
 
 
Figure 14: Scenario A 
Figure 15: Scenario B 
Figure 16: Scenario C 
 Scenario A highlights the competitive effects among secondary consumers. The reintro-
duction of secondary consumers reduced predation pressure on primary consumers but 
also led to inhibitory interactions between populations. 
 Scenario B reflects the complex impact of diversified reintroduction of secondary con-
sumers on energy flow within the system, resulting in significant fluctuations in consumer 
populations. 
 Scenario C demonstrates the significant regulatory effect of reintroduced species on pri-
mary consumer populations, particularly in suppressing pest population fluctuations, 
which indirectly enhanced the competitive advantage of crops. 
6 Analysis of Chemical Dependency and Biodiversity Synergy 
To investigate the impact of human decisions on agroecosystems, we analyzed two aspects: 
reducing chemical dependency and enhancing biodiversity synergy. Regarding chemical de-
pendency, based on Assumption 2, herbicides are deemed necessary during the early stages 
of forest-to-farmland conversion to control weeds. However, as the ecosystem matures, herb-
icide use should be gradually reduced and eventually discontinued. For biodiversity syn-
ergy, we extended bats' ecological role to include pollination and introduced frogs as an alter-
native species. A quantitative analysis of the stability and resilience of both species was con-
ducted to assess their respective contributions. 
6.1 Herbicide Dependency Reduction 
For modeling the reduction of herbicide dependency, we based our approach on Assump-
tion 2, which states that in the first year of the agroecosystem, herbicides are fully relied upon 
to control weed expansion. It is assumed that the herbicide usage remains constant in the second 
~~~~

## 第 017 页

[查看原页版式](pages/page-017.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 17 of 25 
 
year. As the ecosystem matures, starting from the second year, the use of herbicides gradually 
decreases, completely ceasing by the fourth year. To describe this dynamic process, we devel-
oped a time-dependent herbicide reduction model as follows: 
𝑓𝑓her (𝑡𝑡) =
⎩
⎨
⎧1,
0 ≤𝑡𝑡< 𝑇𝑇start 
1 −𝑡𝑡−𝑇𝑇start 
𝑇𝑇reduce 
,
𝑇𝑇start ≤𝑡𝑡< 𝑇𝑇end 
0,
𝑡𝑡≥𝑇𝑇end 
, 
( 18 ) 
where, 𝑓𝑓her (𝑡𝑡) represents the herbicide usage at time 𝑡𝑡; 𝑇𝑇start = 24 marks the starting time of 
herbicide reduction (Year 2); 𝑇𝑇reduce = 36 denotes the duration of reduction (Years 2-5, a total 
of 3 years); and 𝑇𝑇end = 60 is the time when herbicide usage completely stops (Year 5). 
6.2 Biodiversity Synergy 
For modeling biodiversity synergy, we introduced bats as pollinators to enhance crop 
productivity. To achieve this, we modified the crop productivity function in the producer model 
to incorporate the positive contribution of pollination efficiency. Additionally, to analyze the 
role of alternative species, we selected frogs as a substitute to study their performance in pest 
control and ecological balance restoration. Finally, to comprehensively quantify the impact of 
bats and frogs on agroecosystems, we used a system resilience index to analyze the recovery 
time and dynamic characteristics of the system after disturbances. 
For the enhancement of crop productivity by bats' pollination, we expressed the modified 
crop productivity function as: 
𝑟𝑟𝑃𝑃
𝑏𝑏= 𝑟𝑟𝑃𝑃+ 𝛾𝛾bat𝐶𝐶bat, 
( 19 ) 
where, 𝑟𝑟𝑃𝑃
𝑏𝑏 : Crop productivity after the introduction of bats. 𝑟𝑟𝑃𝑃 : Baseline crop productivity. 
𝛾𝛾bat  : Productivity gain coefficient from bats' pollination. 𝐶𝐶bat  : Bat population density. 
For the impact of frogs as a substitute for bats on the system, considering their influence 
on the soil, we adjusted the dynamic carrying capacity 𝐾𝐾(𝑥𝑥, 𝑡𝑡) to include the effect of the 
substitute species: 
𝐾𝐾(𝑥𝑥, 𝑡𝑡) = 𝐾𝐾0 + 𝜙𝜙𝐷𝐷𝐷𝐷+ 𝜆𝜆𝐶𝐶ℎ
fer −𝛽𝛽1𝐶𝐶ℎ
her −𝛽𝛽2𝐶𝐶ℎ
ins + 𝛾𝛾𝐴𝐴𝐴𝐴(𝑥𝑥, 𝑡𝑡), 
( 20 ) 
where, 𝐴𝐴(𝑥𝑥, 𝑡𝑡) : Frog population density.𝛾𝛾𝐴𝐴 : Positive contribution of frogs to the carrying 
capacity. 
The dynamic equation for the frog population is expressed as: 
∂𝐴𝐴
∂𝑡𝑡= 𝐷𝐷𝐴𝐴∇2𝐴𝐴+ 𝑟𝑟𝐴𝐴𝐴𝐴൬1 −𝐴𝐴
𝐾𝐾𝐴𝐴
൰−𝛼𝛼1𝐴𝐴𝐶𝐶1 −𝛼𝛼2𝐴𝐴𝐷𝐷, 
( 21 ) 
where, 𝐷𝐷𝐴𝐴 : Diffusion coefficient of frogs. 𝑟𝑟𝐴𝐴 : Growth rate of frogs. 𝐾𝐾𝐴𝐴 : Carrying capacity 
for frogs. 𝛼𝛼1 : Predation efficiency of frogs on primary consumers. 𝛼𝛼2 : Impact of frogs on 
decomposers. 
For the assessment of system stability and resilience, we used the system resilience index 
(Formula 22 ) for quantification: 
𝑅𝑅= න 
𝑡𝑡1
𝑡𝑡0
൥෍ 
𝑛𝑛
𝑖𝑖=1
 𝑤𝑤𝑖𝑖ቆ|𝑁𝑁𝑖𝑖(𝑡𝑡) −𝑁𝑁𝑖𝑖
∗|
𝑁𝑁𝑖𝑖
∗
ቇ
2
൩
1/2
𝑒𝑒−𝛼𝛼(𝑡𝑡−𝑡𝑡0)𝑑𝑑𝑑𝑑 
( 22 ) 
where 𝑅𝑅: System stability and resilience index. 𝑁𝑁𝑖𝑖(𝑡𝑡): Population size of species 𝑖𝑖 at time 𝑡𝑡. 
𝑁𝑁𝑖𝑖
∗: Equilibrium population size of species 𝑖𝑖. 𝑤𝑤𝑖𝑖: Weight coefficient, measuring the relative 
importance of species 𝑖𝑖  to system stability. 𝑛𝑛 : Total number of species in the system. 
𝑒𝑒−𝛼𝛼(𝑡𝑡−𝑡𝑡0): Time decay factor, emphasizing the greater impact of prolonged recovery deviations 
on system stability. 𝛼𝛼: Time decay coefficient, controlling the weight of time. 𝑡𝑡0, 𝑡𝑡1: The time 
~~~~

## 第 018 页

[查看原页版式](pages/page-018.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 18 of 25 
 
when the system is disturbed and the time when it recovers to equilibrium, respectively. 
6.3 Calculated Results 
We evaluated the dynamic effects of the herbicide dependency reduction strategy and bi-
odiversity synergy on crop and consumer populations, as shown in Figures 17 and 18. 
 
Figure 17: Herbicide attenuation results. In this figure, A represents changes in crop popu-
lation dynamics under different herbicide use strategies; B and C represent changes in con-
sumer population dynamics using the herbicide attenuation strategy and the original strategy, 
respectively. 
 
Figure 18: Biodiversity Synergy Results 
Figure 17(A) shows the impact of herbicide usage on crop population dynamics. During 
the full dependency phase (0–24 months), crop growth was significantly suppressed. In the 
~~~~

## 第 019 页

[查看原页版式](pages/page-019.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 19 of 25 
 
gradual reduction phase (25–60 months), crops steadily recovered and exhibited exponential 
growth after 70 months. This demonstrates that reducing herbicide usage moderately can en-
hance ecosystem support capacity and mitigate environmental impacts. Figures 17(B) and 
17(C) compare consumer populations under different strategies. The reduction strategy (Fig-
ure 17(B)) reduced population fluctuations and improved long-term stability, while the original 
strategy (Figure 17(C)) caused greater fluctuations and lower stability. These results highlight 
the importance of herbicide reduction in maintaining ecological balance and resilience. 
Figure 18 compares the effects of bats and frogs on system stability. Bats significantly 
improved crop productivity through pollination, with minimal fluctuations and a resilience in-
dex of 6.42, indicating strong recovery capability. Frogs contributed primarily to pest control 
but caused greater fluctuations due to their impact on soil and decomposers, with a resilience 
index of 5.01, reflecting lower stability. Overall, bats demonstrated superior ecosystem stability 
and sustainability, offering valuable insights for species introduction strategies. 
7 Model II: Comprehensive Organic Management and Planning 
In green agricultural practices, adopting organic farming methods is essential for under-
standing their comprehensive impacts on ecosystems and individual components, including 
pest control, crop health, plant reproduction, biodiversity, sustainability, and economic 
benefits. To address these, we developed the Comprehensive Organic Management and 
Planning (COMAP) model, employing multi-objective nonlinear programming to analyze the 
ecological and economic effects of different organic farming scenarios. 
7.1 Model Preparation 
Before constructing the model, we systematically analyzed various organic farming sce-
narios to assess their potential impacts on ecosystems and agricultural production. These sce-
narios were based on six key dimensions: pest control, crop health, plant reproduction, biodi-
versity, long-term sustainability, and economic benefits. 
Scenario 1: A system without chemical inputs, relying solely on natural ecological bal-
ance and biodiversity for pest control and crop reproduction. While this may cause short-term 
pest population fluctuations, it enhances biodiversity and soil health over the long term. 
Scenario 2: Combines organic fertilizers and biological control measures, using lim-
ited external inputs to improve crop yields while reducing dependence on natural ecosystems. 
Scenario 3: Explores the synergy between diversified cropping systems and ecologi-
cal conservation, implementing practices such as crop rotation, intercropping, and edge habitat 
construction to optimize ecological and economic outcomes. 
These analyses provided essential parameter support for constructing the COMAP model, 
forming the theoretical basis for designing objective functions and defining constraints. 
7.2 Model Construction 
(1) Decision Variables 
To optimize the ecological and economic benefits under organic farming scenarios, we 
define the following decision variables to quantify key strategies and resource allocations in 
agricultural practices: 
𝑥𝑥organic (𝑡𝑡)  : The amount of organic fertilizer input chosen by farmers at time 𝑡𝑡 . 
𝑥𝑥biocontrol (𝑡𝑡) : The intensity of biological control measures (e.g., introduction of natural ene-
mies or use of biopesticides) chosen by farmers at time 𝑡𝑡. 𝑥𝑥buffer (𝑡𝑡) : The area of ecological 
buffer zones (e.g., biological corridors or uncultivated edge habitats) retained or expanded by 
~~~~

## 第 020 页

[查看原页版式](pages/page-020.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 20 of 25 
 
farmers at time 𝑡𝑡. 
(2) Objective Functions 
Our objective functions focus on two core dimensions: ecological benefits and economic 
benefits. 
Ecological benefits are evaluated based on biodiversity, system stability, and pest density 
to assess the ecological health of the system. The objective function is expressed as: 
max 𝐹𝐹1 = න 
𝑇𝑇
0
൫𝑤𝑤1𝐵𝐵(𝑡𝑡) + 𝑤𝑤2𝐷𝐷(𝑡𝑡) −𝑤𝑤3𝑃𝑃pest (𝑡𝑡)൯𝑑𝑑𝑡𝑡, 
( 23 ) 
where: 𝐵𝐵(𝑡𝑡)  : Biodiversity index at time 𝑡𝑡 . 𝐷𝐷(𝑡𝑡)  : System stability value at time 𝑡𝑡 . 
𝑃𝑃pest (𝑡𝑡) : Pest density at time 𝑡𝑡. 𝑤𝑤1, 𝑤𝑤2, 𝑤𝑤3 : Weights representing the relative importance of 
biodiversity, system stability, and pest control, respectively. 
Economic benefits are quantified based on crop yield, market revenue, and the costs of 
chemicals and management to evaluate agricultural economic returns. The objective function 
is expressed as: 
max 𝐹𝐹2 = න 
𝑇𝑇
0
(𝑃𝑃wheats (𝑡𝑡)𝑅𝑅market (𝑡𝑡) −𝐶𝐶(𝑡𝑡))𝑑𝑑𝑑𝑑, 
( 24 ) 
where 𝑃𝑃wheats (𝑡𝑡) : Crop yield at time 𝑡𝑡. 𝑅𝑅market (𝑡𝑡) : Market revenue at time 𝑡𝑡. 𝐶𝐶(𝑡𝑡) : Costs 
of chemicals and management at time 𝑡𝑡. 
(3) Constraints 
To optimize the sustainability of agroecosystems, we propose four constraints encompass-
ing chemical usage, resource allocation, biodiversity, and soil nutrient balance. 
 Constraint 1: Biodiversity Protection. This constraint ensures that the total popu-
lation of species within the ecosystem remains above the minimum biodiversity 
threshold to maintain ecological health: 
෍ 
𝑛𝑛
𝑖𝑖=1
𝑁𝑁𝑖𝑖(𝑡𝑡) ≥𝑛𝑛min, 
( 25 ) 
where 𝑁𝑁𝑖𝑖(𝑡𝑡) : Population size of species 𝑖𝑖 at time 𝑡𝑡. 𝑛𝑛min: Minimum biodiversity threshold. 
 Constraint 2: Soil Nutrient Balance. The deviation between actual and optimal soil 
nutrient levels must remain within an allowable range to ensure that soil functions 
are not disrupted: 
න 
𝑇𝑇
0
ห𝐹𝐹actual (𝑡𝑡) −𝐹𝐹optimal (𝑡𝑡)ห𝑑𝑑𝑑𝑑≤𝜖𝜖, 
( 26 ) 
where 𝐹𝐹actual (𝑡𝑡) : Actual soil nutrient level at time 𝑡𝑡. 𝐹𝐹optimal (𝑡𝑡) : Optimal soil nutrient level 
at time 𝑡𝑡. 𝜖𝜖 : Allowable deviation. 
 Constraint 3: Chemical Usage Reduction. The use of chemicals must follow a time-
decay model to ensure that herbicide application is gradually reduced, protecting the 
ecosystem: 
𝑥𝑥ℎ(𝑡𝑡) ≤𝑓𝑓her (𝑡𝑡), 𝑓𝑓her (𝑡𝑡) = 𝑒𝑒−𝜅𝜅(𝑡𝑡−𝑡𝑡0) 
( 27 ) 
where 𝑥𝑥ℎ(𝑡𝑡) : Herbicide usage at time 𝑡𝑡 . 𝑓𝑓her (𝑡𝑡) : Emission reduction path function. 𝜅𝜅 : 
Decay rate parameter. 
 Constraint 4: Resource Allocation. The total expenditure on organic farming, pred-
ators, and pollinators must be controlled within the budget limit to optimize resource 
utilization: 
𝑥𝑥organic (𝑡𝑡) + 𝑥𝑥biocontrol (𝑡𝑡) + 𝑥𝑥buffer (𝑡𝑡) ≤𝐵𝐵budget  
( 28 ) 
~~~~

## 第 021 页

[查看原页版式](pages/page-021.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 21 of 25 
 
where 𝐵𝐵budget  : Budget constraint. 
7.3 Calculated results 
Definition 2: The COMAP model is defined as a concave model, ensuring strong duality 
between the primal and dual problems. During the solution process, we employed the Lagran-
gian dual method in combination with the 𝜖𝜖-constraint method (the proof is provided in Ap-
pendix Proof 2) [10]. 
To solve the problem, Lagrange multipliers 𝜇𝜇1(𝑡𝑡), 𝜇𝜇2(𝑡𝑡), 𝜇𝜇3(𝑡𝑡), and 𝜇𝜇4(𝑡𝑡) were intro-
duced for each constraint condition. The Lagrangian function is defined as: 
(
)
(
)
(
)
(
)
1
min
1
0
2
0
3
0
4
0
( )
( )
( )
( )
( )
( )
( )
( )
( )
( )
( )
( )
T
n
i
i
T
actual
optimal
T
her
h
T
budget
organic
biocontrol
buffer
L
F
t
n
N t
dt
t
F
t
F
t
dt
t
f
t
x t
dt
t
B
x
t
x
t
x
t
dt
µ
µ
ε
µ
µ
=
=
+
−
+
−
−
+
−
+
−
+
+
∑
∫
∫
∫
∫
 
( 29 ) 
the combined objective function is defined as: 𝐹𝐹= 𝜆𝜆𝐹𝐹1 + (1 −𝜆𝜆)𝐹𝐹2, where 𝜆𝜆 represents the 
trade-off between the two objective functions, balancing ecological and economic benefits. 
For the primal problem, the dual formulation of the COMAP model, referred to as Dual-
COMAP model, is expressed as: 
min𝐿𝐿(𝜇𝜇1, 𝜇𝜇2, 𝜇𝜇3, 𝜇𝜇4) 
𝑠𝑠. 𝑡𝑡. 𝜇𝜇1(𝑡𝑡) ≥0, 𝜇𝜇2(𝑡𝑡) ≥0, 𝜇𝜇3(𝑡𝑡) ≥0, 𝜇𝜇4(𝑡𝑡) ≥0 
Using the ϵ-constraint method, the results of the COMAP model optimization are summa-
rized in Table 3: 
Table 3: COMAP model results 
Parameter 
𝐹𝐹1(N/A) 
𝐹𝐹2(USD/mouth) 
𝜆𝜆 
Value 
243.58 
13484.36 
0.57 
Parameter 
𝑤𝑤1 
𝑤𝑤2 
𝑤𝑤3 
Value 
0.36 
0.29 
0.45 
Table 3 presents the optimization results of the COMAP model. The ecological benefit 
objective value 𝐹𝐹1 reaches 243.58 (dimensionless), indicating significant improvements in bi-
odiversity and system stability. The economic benefit objective value 𝐹𝐹2 is 13,484.36 USD 
per month, reflecting substantial agricultural economic returns. 
The weight coefficients 𝑤𝑤1 = 0.36, 𝑤𝑤2 = 0.29 , and 𝑤𝑤3 = 0.45 emphasize the critical 
impact of pest density on overall ecological benefits. Additionally, the trade-off coefficient 
𝜆𝜆= 0.57 indicates that the model prioritizes ecological objectives over economic goals. 
8 Sensitivity Analysis 
The parameter perturbation method is a commonly used approach to evaluate the sensi-
tivity of model outputs to changes in input parameters. For our FATE model, we applied this 
method to conduct sensitivity analysis. Specifically, we selected fertilizers, insecticides, and 
species mortality rates as perturbation parameters. Sensitivity was assessed using two ap-
proaches: single-parameter perturbation and multi-parameter mixed perturbation. The model 
responses under different scenarios were simulated, and the sensitivity was quantified using 
the Standardized Sensitivity Coefficient (SSC), defined as: 
~~~~

## 第 022 页

[查看原页版式](pages/page-022.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 22 of 25 
 
𝑆𝑆𝑆𝑆𝑆𝑆= Δ𝑌𝑌/𝑌𝑌baseline 
Δ𝑋𝑋/𝑋𝑋baseline 
 
where: 𝑌𝑌 : Model output. 𝑋𝑋 : Input parameter. 𝑌𝑌baseline  : Output value under baseline pa-
rameter settings. 𝑋𝑋baseline:  Baseline parameter value. 
If |𝑆𝑆𝑆𝑆𝑆𝑆| > 1, the model is highly sensitive to the parameter. If |𝑆𝑆𝑆𝑆𝑆𝑆| ≤1, the model is 
not sensitive to the parameter. 
 
Figure 19: Parameter Perturbation Results 
Sensitivity analysis reveals that the FATE model exhibits low sensitivity to single param-
eters such as species mortality rate (d) with an SSC value of 6.35 (Level I). Moderate sensitiv-
ity is observed for fertilizers (fer) and insecticides (ins) (Level II). However, the sensitivity is 
highest for multi-parameter combinations such as fer+ins+d, with an SSC value of 8.28 (Level 
III). These results indicate that the synergistic effects of multiple parameters significantly in-
fluence system dynamics, highlighting the need to focus on their interactions to optimize eco-
logical management strategies. 
9 Strengths and Weaknesses 
9.1 Strengths 
 
Model I: The FATE model allows for flexible configuration of chemical dependency re-
duction strategies and biodiversity synergy plans by adjusting weights, enabling adapta-
tion to varying regional or climatic conditions. This offers more targeted solutions for 
practical applications. 
 
Model II: The COMAP model balances agroecosystem sustainability and economic re-
turns through multi-objective optimization of ecological (e.g., biodiversity, system stabil-
ity) and economic benefits (e.g., crop yield, market revenue), providing scientific support 
for organic agricultural management. 
9.2 Weaknesses 
 
Model I & II: Both models require high accuracy for ecological and economic parameters 
(e.g., crop yield, biodiversity index, pest density). However, these parameters are often 
influenced by various uncertainties in real agricultural environments, which increases the 
complexity of model application and the risk of errors. 
~~~~

## 第 023 页

[查看原页版式](pages/page-023.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 23 of 25 
 
10 Conclusion 
Using the FATE and COMAP models, we analyzed the impacts of chemical use, species 
regression, biodiversity synergy, and organic agriculture optimization on agroecosystems. Op-
timized chemical strategies were critical for balancing ecological stability and crop productiv-
ity, while species reintroduction required pest management to enhance long-term stability. 
Gradual herbicide reduction promoted crop growth and stabilized consumer populations, with 
bats showing higher resilience through pollination compared to frogs' pest control. The CO-
MAP model effectively balanced ecological and economic goals, highlighting the importance 
of biodiversity and pest density in system performance. These findings provide valuable in-
sights for sustainable agricultural management. 
References 
[1] Abhilash, P. C., & Singh, N. (2009). Pesticide use and application: An Indian sce
nario. Journal of Hazardous Materials, 165(1–3), 1–12. https://doi.org/10.1016/j.jhaz
mat.2008.10.061 
[2] Sokame, B. M., Runyu, J. C., & Tonnang, H. E. Z. (2024). Integrating edible inse
ct into circular agriculture for sustainable production. Sustainable Production and 
Consumption, 52, 80–94. https://doi.org/10.1016/j.spc.2024.10.015 
[3] Pérez-Roig, C., Videla, M., El Mujtar, V., Tittonell, P. A., & Potapov, A. M. (202
5). Soil food-web energy fluxes reveal diverse responses to smallholder land-use c
hoices in temperate forests. Soil Biology and Biochemistry, 200, 109619. https://do
i.org/10.1016/j.soilbio.2024.109619 
[4] Han, X., Wang, X., Cao, Z., Hu, G., Yu, P., He, S., Yan, J., Ganjurjav, H., & Ga
o, Q. (2024). Warming decreased plant litter decomposition by modulating soil fau
na interactions in a Tibetan alpine meadow. Science of The Total Environment, 95
4, 176332. https://doi.org/10.1016/j.scitotenv.2024.176332 
[5] Bravo, A.S., Camps, S.P., Pérez, M.Á.V., et al. 2024. Soil ecosystem services valu
ation in a priority terrestrial region for biodiversity conservation in Mexico, from 
ecological economics and the local community perspective. Discover Sustainability. 
5: 457. https://doi.org/10.1007/s43621-024-00691-8 
[6] USDA National Agricultural Statistics Service (NASS). United States Department o
f Agriculture. Available at https://www.nass.usda.gov. 
[7] National Centers for Environmental Information (NCEI). National Oceanic and At
mospheric Administration (NOAA). Available at https://www.ncei.noaa.gov. 
[8] Natural Resources Conservation Service (NRCS). Soil Survey, United States Depart
ment of Agriculture. Available at https://www.nrcs.usda.gov. 
[9] Blasius, B., Huppert, A., & Stone, L. (1999). Complex dynamics and phase synch
ronization in spatially extended ecological systems. Nature, 399, 354–359. https://d
oi.org/10.1038/20676 
[10] de Ruiter, F. J. C. T., Zhen, J., & den Hertog, D. (2022). Dual approach for two
-stage robust nonlinear optimization. Operations Research, 71(5), 1794–1799. https:/
/doi.org/10.1287/opre.2022.2289 
[11] Scholtes, S. (2004). Nonconvex structures in nonlinear programming. Operations R
esearch, 52(3), 368–383. https://doi.org/10.1287/opre.1030.0102 
~~~~

## 第 024 页

[查看原页版式](pages/page-024.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
          Page 24 of 25 
 
Appendices 
Proof 1: Mathematical Expression of Spatial Dimensions 
To prove Definition 1, we employ the following lemmas: 
Lemma 1 (Fick's First Law): Describes the relationship between diffusion flux and con-
centration gradient, expressed as 𝐽𝐽= −𝐷𝐷𝛻𝛻𝑃𝑃(𝑥𝑥, 𝑡𝑡), where 𝐽𝐽 is the diffusion flux, −𝐷𝐷 is the 
diffusion coefficient, and 𝛻𝛻𝑃𝑃(𝑥𝑥, 𝑡𝑡) is the gradient of population density. 
Lemma 2 (Continuity Equation): Describes the conservation of mass, expressed as 
𝜕𝜕𝑃𝑃(𝑥𝑥,𝑡𝑡)
𝜕𝜕𝑡𝑡
+ 𝛻𝛻𝐽𝐽= 0, indicating that the rate of change of population density over time equals the 
net change in influx and outflux. 
From Lemma 1, the diffusion flux 𝐽𝐽 is defined as: 
𝐽𝐽= −𝐷𝐷∇𝑃𝑃(𝑥𝑥, 𝑡𝑡), 
where ∇𝑃𝑃(𝑥𝑥, 𝑡𝑡) represents the spatial gradient of population density, and −𝐷𝐷 indicates that 
diffusion occurs from high-density to low-density regions. 
Substituting 𝐽𝐽 into the continuity equation (𝐋𝐋𝐋𝐋𝐋𝐋𝐋𝐋𝐚𝐚 𝟐𝟐): 
∂𝑃𝑃(𝑥𝑥, 𝑡𝑡)
∂𝑡𝑡
+ ∇(−𝐷𝐷∇𝑃𝑃(𝑥𝑥, 𝑡𝑡)) = 0 ⇒∂𝑃𝑃(𝑥𝑥, 𝑡𝑡)
∂𝑡𝑡
= 𝐷𝐷∇(∇𝑃𝑃(𝑥𝑥, 𝑡𝑡)) = 𝐷𝐷∇2𝑃𝑃(𝑥𝑥, 𝑡𝑡) 
Thus, the spatial diffusion term ∇2𝑃𝑃(𝑥𝑥, 𝑡𝑡) fully characterizes the spatial dynamics of spe-
cies population density. 
Proof 2: Concavity of the COMAP Model 
To prove Definition 2, we use the following lemmas: 
Lemma 3 (Concavity of Weighted Sums): If 𝑓𝑓𝑖𝑖(𝑥𝑥) is concave and 𝑤𝑤𝑖𝑖≥0 , then the 
weighted sum 𝑓𝑓(𝑥𝑥) = ∑𝑖𝑖 𝑤𝑤𝑖𝑖𝑓𝑓𝑖𝑖(𝑥𝑥) is also concave. 
Lemma 4 (Concavity of Integration): If 𝑓𝑓(𝑥𝑥, 𝑡𝑡) is concave with respect to 𝑥𝑥, and the 
integration interval is fixed, then the integral ∫𝑎𝑎
𝑏𝑏 𝑓𝑓(𝑥𝑥, 𝑡𝑡)𝑑𝑑𝑑𝑑 is also concave with respect to 𝑥𝑥. 
(1) Concavity of 𝑭𝑭𝟏𝟏 
𝐹𝐹1 is defined as the integral of three components: biodiversity 𝐵𝐵(𝑡𝑡) , system stability 
𝐷𝐷(𝑡𝑡) , and pest density 𝑃𝑃pest (𝑡𝑡) . Biodiversity 𝐵𝐵(𝑡𝑡) = ∑𝑖𝑖=1
𝑛𝑛 𝑁𝑁𝑖𝑖(𝑡𝑡) : 𝑁𝑁𝑖𝑖(𝑡𝑡) follows the dy-
namic competition equation: 
∂𝑁𝑁𝑖𝑖(𝑡𝑡)
∂𝑡𝑡
= 𝑟𝑟𝑖𝑖𝑁𝑁𝑖𝑖(𝑡𝑡) ൬1 −𝑁𝑁𝑖𝑖(𝑡𝑡)
𝐾𝐾𝑖𝑖
൰−෍ 
𝑗𝑗≠𝑖𝑖
𝛽𝛽𝑖𝑖𝑖𝑖𝑁𝑁𝑖𝑖(𝑡𝑡)𝑁𝑁𝑗𝑗(𝑡𝑡) 
where 𝐾𝐾𝑖𝑖≥0 and 𝛽𝛽𝑖𝑖𝑖𝑖≥0. Since 𝑁𝑁𝑖𝑖(𝑡𝑡) is governed by a logistic growth equation, it is con-
cave. Consequently, 𝐵𝐵(𝑡𝑡) , as a summation, is concave. System Stability 𝐷𝐷(𝑡𝑡) =
−ln (𝜎𝜎2(𝑡𝑡) + 1) : Variance 𝜎𝜎2(𝑡𝑡) is a convex function, and −ln (𝑥𝑥) is concave. Therefore, 
𝐷𝐷(𝑡𝑡) is concave. Pest Density 𝑃𝑃pest (𝑡𝑡) : As pest density follows a dynamic equation similar 
to a competition model, it is concave. By Lemmas 3 and 4, with 𝑤𝑤1, 𝑤𝑤2, 𝑤𝑤3 > 0, and given 
𝐹𝐹1 is in integral form, 𝑭𝑭𝟏𝟏 is concave. 
(2) Concavity of 𝐹𝐹2 
𝐹𝐹2 is defined as the difference between crop yield, market revenue, and cost: 
Crop Yield 𝑃𝑃wheats (𝑡𝑡) = ln (1 + 𝑁𝑁wheats (𝑡𝑡)) : Since ln (𝑥𝑥) is concave, 𝑃𝑃wheats (𝑡𝑡) is 
concave. Market Revenue 𝑅𝑅market (𝑡𝑡) : Given that crop market prices are relatively stable, 
𝑅𝑅market (𝑡𝑡) can be approximated as a linear function and is convex. Cost 𝐶𝐶(𝑡𝑡) = 𝛽𝛽𝑡𝑡2 : 𝐶𝐶(𝑡𝑡) 
is convex, but its negative −𝐶𝐶(𝑡𝑡) is concave. By combining these terms, 𝑭𝑭𝟐𝟐 is concave. 
~~~~

## 第 025 页

[查看原页版式](pages/page-025.jpg)

~~~~text
Topic: Recommendations for Organic Farming Practices
Form：Team # 2508861 of 2025 ICM
Date：January 28, 2025
To our farmer friends
Dear Farmers,
Sustainable organic agriculture can not only effectively control pests, improve soil health, and enhance
biodiversity, but also create economic benefits in the ever-expanding organic market. Therefore, we have
specially written this letter to provide you with recommendations for exploring organic farming practices.
The transition to organic farming requires initial investments, such as organic fertilizers and biological
pest control. These measures effectively control pests, reduce the use of chemicals, and enhance soil fertility,
leading to long-term returns. Its sustainability is reflected in improved ecological resilience, enhanced soil
productivity, and reduced environmental impact. Therefore, a positive cycle between economics and
sustainability requires our collective effort.
We sincerely hope that these suggestions will help you find the best balance between economics and
ecology in practice, and together, we can work towards a healthier agricultural ecosystem.
Yours sincerely,
Team # 2508861
~~~~

## 第 026 页

[查看原页版式](pages/page-026.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
                       26   
 
Report on Use of AI 
 
 
 
 
 
GPT-4o
Query1: What is the difference between forest ecosystems and agro-ecosystems?
Output:
There are many significant differences between forest ecosystems and agro-ecosystems 
in terms of structure, function, species diversity and ecological processes. The following are 
their major differences: 
1. Species Diversity 
Forest ecosystems: Forest ecosystems usually have a high species diversity. This in-
cludes different types of plants, animals, microorganisms, and complex interactions between 
them. Species in forests have strong mutually beneficial symbiotic, competitive and preda-
tory relationships that form highly complex food chains. 
Agroecosystems: Agroecosystems are more homogenous in species, consisting mainly 
of crops, weeds, pests, and other plants grown or managed by farmers. Species diversity is 
usually low due to high human intervention, and many ecological processes (e.g., pollina-
tion, soil fertility maintenance, etc.) often depend on external inputs such as fertilizers and 
pesticides. 
2. Ecological Processes 
Forest ecosystems: Forests maintain ecological balance through the natural carbon, ni-
trogen and water cycles. Forest soils are rich in organic matter, maintain high soil fertility, 
and have a strong ability to regulate water sources. Forests also absorb large amounts of 
carbon dioxide through photosynthesis by trees and plants. 
Agroecosystems: Ecological processes in agroecosystems are usually highly influenced 
by human intervention. Crops have short growth cycles and soil management (e.g., fertili-
zation, irrigation) has a greater impact on the soil, which can easily lead to soil degradation, 
infertility, or salinization. Agricultural activities usually result in rapid depletion of soil wa-
ter, nutrients and organic matter. 
3. Productivity and biomass 
Forest ecosystems: Forests typically have high annual productivity and a long-term ca-
pacity to store carbon. Forests provide abundant biomass, including trees, shrubs, and herbs, 
and material cycling is more stable in forest ecosystems. 
Agricultural ecosystems: The productivity of agricultural land is usually more concen-
trated and cyclical, and is largely dependent on human management and technology (e.g., 
irrigation, fertilization, etc.). In contrast to forests, the biomass of farmland is concentrated 
in the crops themselves, and the long-term productivity of the soil often depends on external 
replenishment. 
 
Query2: What aspects need to be considered for the development of sustainable organic agri-
culture? 
Output: 
 
The development of sustainable organic agriculture requires a combination of aspects 
~~~~

## 第 027 页

[查看原页版式](pages/page-027.jpg)

~~~~text
TEAM # 2508861 
 
 
 
 
 
 
 
 
 
 
 
 
                       27   
 
to ensure the long-term environmental, social and economic sustainability of agricultural 
production. The following are some of the key considerations: 
1. Soil Health and Management 
Organic Fertilizers and Compost: Organic agriculture emphasizes the use of natural 
fertilizers (e.g. compost, green manure, animal manure, etc.) rather than chemical fertilizers 
to increase the organic matter content of the soil and to enhance soil fertility and structure. 
Crop Rotation and Intercropping: Crop rotation (rotation of different crops) and inter-
cropping (mixing of different crops) help to break the cycle of pests and diseases while 
maintaining a balance of soil nutrients and avoiding over-dependence on a single crop. 
Reducing Soil Erosion: Reducing soil erosion through the use of cover crops, conser-
vation tillage, etc. improves the water retention capacity and biological activity of the soil. 
2. Biodiversity Conservation 
Ecosystem Services: Conservation and enhancement of biodiversity is essential in or-
ganic agriculture. This includes maintaining and restoring wildlife habitats, promoting spe-
cies diversity (e.g., beneficial insects, pollinators, etc.), and providing ecological buffer 
strips by planting a diversity of plants along farm boundaries. 
Reducing the Impact of Pests and Diseases: Reduce pest and disease damage without 
relying on chemical pesticides by introducing beneficial insects (e.g., bees, bats, etc.), culti-
vating pest-resistant crop varieties, and using biopesticides or physical means of control. 
3.Reducing Chemical Dependency 
Control of Fertilizer and Pesticide Use: Sustainable organic agriculture requires avoid-
ing the use of chemical fertilizers and pesticides altogether, and instead managing crop 
growth and controlling pests and diseases through natural methods (e.g., compost, plant-
based fertilizers, natural pesticides, etc.). 
Natural Enemy Utilization: Control of pest populations with the help of natural preda-
tors, parasites, or microorganisms, thus reducing reliance on chemicals. 
4.Water Resources Management 
Water Saving Irrigation Technology: Adoption of drip irrigation, sprinkler irrigation, 
and other efficient water resource utilization technologies to reduce water evaporation and 
wastage, and to ensure sustainable use of water for agriculture. 
Rainwater Harvesting and Management: Ensure water supply during the dry season by 
constructing rainwater harvesting systems, cisterns, and other measures. 
Soil water retention: Improve the water retention capacity of the soil and reduce water 
loss by means of cover crops and deep plowing. 
 
~~~~
