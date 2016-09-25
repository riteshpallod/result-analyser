library(shiny)
library(ggplot2)
library(RSQLite)
#######################read-me#########or-not###############lul############################################
#Almost every function or every section of code has a similar block of code,
#the block which changes the subject name to subject code or in same cases eventually
#in subject-code+TYPE format.
#
#Why? Because data, marks, are stored in columns which have their(thier) names encoded as codeType.
#But we need to display the subject names instead, also without types. And the 'type' will also be an input.
#another input.
#Bottom line: data = stored as= codeType
#             data = retrived as= name + type
##########################################################################################################


###################imp####################################################################################
#         match = gets the index number of the common element; one arg is element, another vector, list.
#         unique = gets the unique elements from the vecor
#         paste = when we need to concat strings; concatenation of shit
#         PS : matrix, if found in variable name, does not mean that the variable is a matrix
#             same can be said about list, array.
###########################################################################################################

x="se_ledger_m16"
ex1<-"pdf"
ex2<-"txt"
x1<-paste(x,ex1,sep=".")
comm="python pyth1.py"
comm1<-paste(comm,x1,sep=" ")
system(comm1)
x2<-paste(x,ex2,sep=".")
comm="python 2pyth.py"
comm1<-paste(comm,x2,sep=" ")
system(comm1)
comm="python combi3plus5_brand_new_1.py"
comm1<-paste(comm,x2,sep=" ")
system(comm1)
my_codes <- c("anmva","aajd")
#subject code for sem1 in datFrame
sqlite<-dbDriver("SQLite")
mysqlconnection = dbConnect(sqlite,dbname="test.db")
atab <- dbListTables(mysqlconnection)
result = dbSendQuery(mysqlconnection, "select * from subjectcodes_sem1")
datFrame1 = fetch(result)

result = dbSendQuery(mysqlconnection, "select * from sem1")
D1 = fetch(result)

#unique subjects, for select inputs, index will be same.
#these fields below will help us display the 'select subject' part in our ui,
#and also when we need to #convert the subject_name back to subject_code
#(subject have same index in the vectors below), as the database has marks according to 'code+TYPE' format

codes_unique1 <- unique(datFrame1[,1])
sub_unique1 <- unique(datFrame1[,3])

yes_sem2= TRUE

#this function is to make sure you have to two sems, in the PDF. 'atab' has all the tables
if (is.na(match("sem2", atab))){
  yes_sem2 = FALSE
}


#if the 'sem2' table is present, we need to create similar arrays, vectors, dataframes, for sem2.
codes_unique2 <- c()
sub_unique2 <- c()
datFrame2 <- data.frame()
D2 <- data.frame()
if (yes_sem2) {
  #make D2,datFrame2
  #same old stuff. append a 2!
  result = dbSendQuery(mysqlconnection, "select * from subjectcodes_sem2")
  datFrame2 = fetch(result)

  result = dbSendQuery(mysqlconnection, "select * from sem2")
  D2 = fetch(result)
  codes_unique2 <- unique(datFrame2[,1])
  sub_unique2 <- unique(datFrame2[,3])
}

#these functions give us the proper dataframe or vector, according to semester, which is the parameter
get_codes_unique <-function(sem){
  if (sem == 1){
    return (codes_unique1)
  }
  return (codes_unique2)
}

get_sub_unique <-function(sem){
  if (sem == 1)
    return (sub_unique1)
  return (sub_unique2)
}

get_D <- function (sem){ #D has the actual semester table, the one with the marks
  if (sem == 1)
    return (D1)
  return (D2)
}

get_datFrame <- function(sem){ #datFrame has subject information
  if (sem == 1)
    return (datFrame1)
  return (datFrame2)
}

#distinction, firstclass, secondclass, third class, ST, SC, other shit.
get_percent_number <- c(0.66,0.6,0.55,0.5,0.4)

#function to get select input types
#this little pos gives us (returns) an array with all types in it
#we pass datframe, and string; string is the subject_name, from the ui (read select_subject).
get_types <- function (string,datFrame){
  typ1 <- c()
  for (i in 1:nrow(datFrame)){
    if (string==datFrame[i,3])
      typ1 <- c(typ1, datFrame[i,2])
  }
  typ1 <- c(typ1, "ALL")
  return(typ1)
}

#need documnentation, but basically it returns total
#OKAY, THIS IS USELESS, TOO MANY FUNCTION CALLS, INSTEAD OF THIS WE CAN CREATE A FUNCTION WHICH CREATES AN DATAFRAME OF ALL THOSE VECTORS.
#HOW?
get_all_matrix <- function (sub_string,sem,datFrame){
  sub_unique <- get_sub_unique(sem)
  codes_unique <- get_codes_unique(sem)
  D <- get_D(sem)

  buf1 <- match(sub_string, sub_unique)
  sub_code <- codes_unique[buf1]

  all_matrix <- c()
  sub_type <- get_types(sub_string,datFrame)
  #print (sub_type)
  for (l in 1:(length(sub_type)-1)){
    fin1_x <- paste(sub_code,sub_type[l],sep = "")
    print (l)
    print (fin1_x)
    if (l == 1){
      all_matrix <- D[,fin1_x]
    }
    else {
      all_matrix <- all_matrix + D[,fin1_x]
    }
  }
  return(all_matrix)
}

#dummys to call
#THIS CALLS THE ABOVE FUNCTION.
#INSTEAD IT SHOULD RETURN THE VALUE FROM THAT DATAFRAME
get_all_sem_respective <- function(sub_string, sem){
  if (sem == 1){
    get_all_matrix(sub_string,sem,datFrame1)
  }
  else {
    get_all_matrix(sub_string,sem,datFrame2)
  }
}


#this creates a vector with MAX MARKS values. Including "all"'s
#okay, now we need to have a max marks vector for the 'class' output
#also use this while printing the graph
create_arr <- function(datFrame,sem){
  codes_unique <- get_codes_unique(sem)
  sub_unique <- get_sub_unique(sem)

  arr <- c()
  for (i in (1:nrow(datFrame))){
    buff_code <- paste(datFrame[i,1],datFrame[i,2],sep="")
    arr[buff_code] <- datFrame[i,4]
  }

  for (j in (1:length(codes_unique))) {
    buff <- codes_unique[j]
    buff_str <- sub_unique[j]
    typ <- get_types(buff_str,datFrame)

    buff_all <- paste(buff,"ALL", sep = "")
    for (k in (1:(length(typ)-1))){
      buff_codeT <- paste(buff,typ[k],sep = "")
      if (k == 1){
        arr[buff_all] <- arr[buff_codeT]
      }
      else {
        arr[buff_all] <-arr[buff_all] + arr[buff_codeT]
      }
    }

  }
  return(arr)
}

#this is what I was talking about
#dynamo_total has those direct total values, and the below function returns total ahen a "codeType" is an arg
dynamo_total1 <- create_arr(datFrame1,1)
dynamo_total2 <- c()
if (yes_sem2){
  dynamo_total2 <- create_arr(datFrame2,2)
}


get_respective_total <- function(direct_hyb,sem){
  if (sem == 1){
    return(dynamo_total1[direct_hyb])
  }
  return(dynamo_total2[direct_hyb])

}

ui <- shinyUI(fluidPage(

  navbarPage("Result Analyser",
             tabPanel("Semester",
                      sidebarLayout(
                        sidebarPanel(
                          selectInput("select_sem", label = "Select Sem!",
                                      choices = list(SEM1 = 1, SEM2 =2)),
                          uiOutput("sele_sub"),
                          uiOutput("sele_type"),
                          hr(),
                          h4("Classes!"),
                          fluidRow(column(12, verbatimTextOutput("distinction_c"))),
                          fluidRow(column(12, verbatimTextOutput("first_c"))),
                          fluidRow(column(12, verbatimTextOutput("Hsecond_c"))),
                          fluidRow(column(12, verbatimTextOutput("second_c"))),
                          fluidRow(column(12, verbatimTextOutput("pass_c")))
                        ),
                        mainPanel(
                          plotOutput("plotG1")
                        )
                      )),
             navbarMenu("More",
                        tabPanel("Student Information"))
  )

  # Sidebar with a slider input for number of bins

))

# Define server logic required to draw a histogram
server <- shinyServer(function(input, output) {

  #this is select input for type
  output$sele_sub <- renderUI({
    selectInput("select_subject", label = "Select Subject!",
                choices = get_sub_unique(input$select_sem))
  })

  output$sele_type <- renderUI({
    selectInput("select_type", label= "Select Type!",
                choices = get_types(input$select_subject,get_datFrame(input$select_sem)))
  })




  data_dum_dist <- function(print_dist_or_other)({
    #print_dist_or_other argument is the 'class' vector index

    #for 'distinction and other classes' output

    sub_unique <- get_sub_unique(input$select_sem)
    codes_unique <- get_codes_unique(input$select_sem)
    D <- get_D(input$select_sem)

    #get index. get code.
    buf <- match(input$select_subject, sub_unique)
    code_x <- codes_unique[buf]

    #NOW FOR 'ALL' WE DONT HAVE INDEX. WHAT NOW?
    ty1 <- input$select_type
    fin_x <- paste(code_x,ty1,sep = "")

    #getting and 'counting' marks
    if (ty1 == "ALL"){
      x_mark <- get_all_sem_respective(input$select_subject,input$select_sem)
      #x_mark <- (D2[,fin_x])
    }
    else {
      x_mark <- (D[,fin_x])
    }

    len_x <- length(which(x_mark > get_percent_number[print_dist_or_other]*get_respective_total(fin_x, input$select_sem)))
    len_x
  })

  #instead of using 5 datas, we can use 1. I guess. Gave it a try. Something went wrong. No time for this stuff. Will check later.
  data <- reactive({
    data_dum_dist(1)
  })
  data_2 <- reactive({
    data_dum_dist(2)
  })
  data_3 <- reactive({
    data_dum_dist(3)
  })
  data_4 <- reactive({
    data_dum_dist(4)
  })
  data_5 <- reactive({
    data_dum_dist(5)
  })

  output$distinction_c <- renderText({
    c("Distinction :",data())
  })
  output$first_c <- renderText({
    c("First Class :",data_2()-data()) # so if dist is 10 and second class (accord to above logic) is 30, then actual dist is 10, second class is 20. SO YOU GOTTA MINUS THAT SHIT.
  })
  output$Hsecond_c <- renderText({
    c("Higher Secondary Class :",data_3()-data_2())
  })
  output$second_c <- renderText({
    c("Secondary Class :",data_4()-data_3())
  })
  output$pass_c <- renderText({
    c("Pass: ",data_5()-data_4())
  })

  output$plotG1 <- renderPlot({
    #no need for this pos. Will change later
    sub_unique <- get_sub_unique(input$select_sem)
    codes_unique <- get_codes_unique(input$select_sem)

    buf1 <- match(input$select_subject, sub_unique)
    sub_code <- paste(codes_unique[buf1],"ALL",sep = "")
    #need to do something
    x1 <- get_all_sem_respective(input$select_subject,input$select_sem)

    qplot(x1, geom="histogram",binwidth = 0.5,
          main = "marks v number of students",
          xlab = "marks",
          fill=I("blue"),
          col=I("black"),
          alpha=I(.2),
          xlim=c(50,175),#add a total function
          ylim = c(0,25))
  })
  output$value1 <- renderPrint({ input$select_subject })
  output$value2 <- renderPrint({ input$select_type })

})

# Run the application
shinyApp(ui = ui, server = server)
