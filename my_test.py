from main import ServiceFunnel

###---test html---###
html_string = """
            <article class="article " id="id-39334" data-tags="A,B,C"><h2>S1</h2></article>
            <article class="article " id="id-39335" data-tags="A,B,D,E"><h2>S2</h2></article>	
            <article class="article " id="id-39336" data-tags="X,C,D,L"><h2>S3</h2></article>
            <article class="article " id="id-39337" data-tags="J,A,B,Q"><h2>S4</h2></article>
            <article class="article " id="id-39338" data-tags="M,A,B,C,S"><h2>S5</h2></article>

        """
service_funnel = ServiceFunnel()
service_funnel.scrape_html(html_string)


def test_valid_tags_with_snippet():
	result = service_funnel.handle_request(
            {"selected_tags": [{"name": "A"}, {"name": "B"}, {"name": "C"}]}       
	return result												

def test_invalid_tags():
	result = service_funnel.handle_request(
            {"selected_tags": [{"name": "W"}, {"name": "T"}, {"name": "R"}]}	   
        )
	return result

def test_valid_tags_without_snippet():
	result = service_funnel.handle_request(
            {"selected_tags": [{"name": "A"}, {"name": "B"}]}					    
        )													
	return result

def test_valid_tags_without_snippet_onematch():
	result = service_funnel.handle_request(						
            {"selected_tags": [{"name": "X"}, {"name": "C"}, {"name": "D"}]}		
        )
	return result

	


if __name__ == "__main__":
	print('\n' '-----------test_valid_tags_with_snippet------------' '\n' )
	print(test_valid_tags_with_snippet() )
	print('\n' '\n' '----------test_invalid_tags------------------------' '\n' )
	print(test_invalid_tags())
	print('\n' '\n' '-----------test_valid_tags_without_snippet--------' '\n' )
	print(test_valid_tags_without_snippet())
	print('\n ' '\n' '------test_valid_tags_without_snippet_onematch----' '\n' )
	print(test_valid_tags_without_snippet_onematch())

    
