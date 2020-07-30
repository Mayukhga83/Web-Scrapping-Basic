import argparse


class ServiceFunnel:
    def __init__(self):
      self.mydict = {}    # dictionary for storing snippets with tags as key after scraping
                          # called on the API for checking match
        
####################--------------SCRAPING METHOD------------###################
    def scrape_html(self, html: str):
      
      mylist = html.split('article>')  ###---split for snippet separation---###
  
# scrap the data tags and update to dictionary
      for i in range(len(mylist)):
        if 'data-tags' in mylist[i]:  # check if datatag present
          split_snippet = mylist[i].split('data-tags=')
          tag = split_snippet[1].split('>')     # get the tags

          ########----delete "" and , from tags------#######---and store as tuple key
          j = tuple(tag[0].replace('"', '').replace(',', ' ').split())
          self.mydict.update({j : mylist[i] + 'article>'})  # update mydict
          
      return self.mydict
########################-----------END-------------------#########################  


#######################---------API FUNCTIONALITY--------#########################
    def handle_request(self,request: dict) -> dict:

# create tap tuple of request to check with mydict
      request_taglist = []  
      for tag in request["selected_tags"]:     
          request_taglist.append(tag['name'])
      j = tuple(request_taglist)

      
###---------OUTPUT DICTIONARY-----######
      output_dict = {
          "snippet": None,
          "next_tags": [],
          "status": {
              "code": 2,
              "msg": "Invalid tags"
          },
          "selected_tags": [{                   ## Default Output for No Match ##
              "name": "Some"
          }, {
              "name": "Invalid"
          }, {
              "name": "Combo"
          }]
      }

####----------LOGIC FOR API-----------####
      nextags = []
      Flag_match = False
      Flag_possible = False
      count_matched = 0
      
# check for match
      for items in self.mydict.keys():      
          if set(j) == set(items):      
                                        # Exact match with snippets
              Flag_match = True  

          elif set(j) < set(items):
              for i in set(items) - set(j):
                nextags.append(i)           # Match without snippet
                                            # request tag is contained in one or more tag
              Flag_possible = True
              count_matched += 1     

              
####-------------------OUTPUT FOR EXACT MATCH WITH SNIPPET------------####
      if Flag_match == True:
        output_dict["snippet"] = '</article>' + self.mydict[j].split('h2>')[1].split('</')[0] + '</article>'   # only title snippet
        for i in nextags:                                                                                      #added. replace with
          dic = {'name' : list(i)[0]}                                                                          # mydict[j] for entire
          output_dict["next_tags"].append(dic)   # nextags displayed as dictionary                                                              #snippet
        output_dict["status"]["code"] = 0
        output_dict["status"]["msg"] = 'valid tags with snippet'
        output_dict["selected_tags"] = request["selected_tags"]

####-------------------OUTPUT FOR  1 MATCH WITHOUT SNIPPET------------####

      elif Flag_match == False and Flag_possible == True and count_matched ==1:
        
        request_taglist.extend([x for x in nextags[0]])
        
        output_dict["snippet"] = '</article>' + self.mydict[tuple(request_taglist)].split('h2>')[1].split('</')[0] + '</article>'
        
        for i in nextags:
          dic = {'name' : list(i)[0]}
          output_dict["next_tags"].append(dic)

        output_dict["status"]["code"] = 1
        output_dict["status"]["msg"] = 'valid tags but no snippet'
        output_dict["selected_tags"][0]["name"] = "Not"
        output_dict["selected_tags"][1]["name"] = "Enough"
        output_dict["selected_tags"][2]["name"] = "Tags"

####-------------------OUTPUT FOR MORE THAN 1 MATCH WITHOUT SNIPPET------------####

      elif Flag_match == False and Flag_possible == True and count_matched > 1:
        
        for i in nextags:
          dic = {'name' : list(i)[0]}                               # No snippet as stated in the problem
          output_dict["next_tags"].append(dic)

        output_dict["status"]["code"] = 1
        output_dict["status"]["msg"] = 'valid tags but no snippet'
        output_dict["selected_tags"][0]["name"] = "Not"
        output_dict["selected_tags"][1]["name"] = "Enough"
        output_dict["selected_tags"][2]["name"] = "Tags"

      return output_dict



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--html_path",
        help="path leading to the html file",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    with open(args.html_path, "r") as f:
        html_str = f.read()
    service_funnel = ServiceFunnel()
    service_funnel.scrape_html(html_str)
