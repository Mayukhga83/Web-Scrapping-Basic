# Scrapping and Tag Matching HTML Content with Python
HTML string based web scrapping 

* The End Goal : is to have a website where visitors can click on tags and combine several of these to receive information. A user will land on the page without knowing what they are looking for.The visitors will click on the first tag they see as related to their problem and then choose ever more suitable tags until they reaches their final piece of information they need.

## This Code
* An API handling is built to power this functionality.

Task Includes:

1) Scraping HTML content
2) Implementing API functionality

## Scraping HTML

The HTML contains many elements. The ones relevant are the ones which contain the attribute `data-tags`. There can be multiple different elements containing this attribute. This attribute is a comma separated list of all `tags` relevant to this piece of information. The entire HTML element is what we are concerned about and will return in our API. We shall refer to each html element containing these `data-tags` as a `snippet`. 


## Implementing API functionality

The API works as follows:
Send it a list of selected tags and receive one of 3 types of responses seen below:
1. The given list of selected tags points to a unique snippet
2. The given list of selected tags is valid i.e. it is a subset of a list of
   tags which belong to a snippet
3. The given list of selected tags is invalid, this tag combination exists
   nowhere in the scraped HTML nor is it a subset thereof.

### API Response:

* status - An object with two fields 
    * code - 0,1,2 depending on the use case 
    * msg - explaining the meaning of the code 
* snippet - If one exists a HTML element as json serializable string, else null 
* next_tags - A list of valid tags which the visitor can click on next sorted
    alphabetically by the name field.
* selected_tags - A field to verify that the API used the correct query parameters

### Detailed explanation of logic

Suppose the HTML contains the following snippets and tags mapping:
```
“S1” with tags “A”

“S2” with tags “A” “B” “C”

“S3” with tags “A” “B” “D”

“S4” with tags “A” “D” “E”
```
1. Given a set of snippets with a set of tags, any subset of these tags is a valid tag combination.
```
"A" "B" is a valid tag set as it is a subset of the tags for "S2" and "S3".
"B" "E" is not a valid tag set as it not a subset of any of the above snippets.
"X" is not a valid tag as it is not present in any of the above snippets.
```
2. Only valid possible tags are shown in the list of next_tags field. 
```
If "B" is selected only "A" "C" "D" are shown as next tags.
If "A" is selected "B" "C" "D" "E" are possible next tags.
```
3. A snippet is only output if the selected tags are an exact match to the tags on the HTML snippet.
```
If "A" is selected, "S1" should be shown.
If "A" "B" "C" is selected snippet "S2" should be shown.
If "A" "B" is selected no snippet should be shown because there's not unique snippet possible in this case.
```
4. A snippet can also be output if there is only one possible snippet which can be reached from the selected tag combination. 
```
If "E" is selected snippet "S4" should be shown. There's no exact match happening in this case and since there's only one possibility we can do fast-forward and assume that the selected tags consisted of "A" "D" "E" instead of just "E". There's also no need to show "A" "D" as next_tags in this case.
```
5. The order of the path taken to get to any snippet is irrelevant.
```
Selecting "C" "B" "A" is the same as selecting "A" "C" "B"
```
