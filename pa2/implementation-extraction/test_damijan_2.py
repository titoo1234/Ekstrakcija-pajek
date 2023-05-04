from extraction_automatic import *
from textdistance import jaccard
from textdistance import damerau_levenshtein

text1 = """<div>
           <div>
            <h3>
             <span>
              #text
             </span>
             <a>
              #text
             </a>
             <span>
              #text
             </span>
            </h3>
            <p>
             <span>
              #text
             </span>
             <span>
              |
             </span>
             <span>
              #text
             </span>
             <span>
              |
             </span>
             <span>
              #text
             </span>
            </p>
            <div>
             <div>
              <strong>
               #text
              </strong>
             </div>
             <div>
              <span>
               Rate this
              </span>
              <div>
               <div>
                <span>
                 1 2 3 4 5 6 7 8 9 10
                </span>
                <span>
                 <span>
                  #text
                 </span>
                 (
                 <span>
                  10
                 </span>
                 ) +
                </span>
                <span>
                 X
                </span>
               </div>
              </div>
             </div>
             <div>
              Metascore
              <span>
               #text
              </span>
             </div>
            </div>
            <p>
             #text
            </p>
            <p>
             Director:Stars:,,,(
             <a>
              #text
             </a>
             ) +
             <span>
              |
             </span>
             (
             <a>
              #text
             </a>
             ) +
            </p>
            <p>
             <span>
              Votes:
             </span>
             <span>
              #text
             </span>
             <span>
              |
             </span>
             <span>
              Gross:
             </span>
             <span>
              #text
             </span>
            </p>
           </div>
          </div>"""
text2 = """<div>
           <div>
            <h3>
             <span>
              #text
             </span>
             <a>
              #text
             </a>
             <span>
              #text
             </span>
            </h3>
            <p>
             <span>
              #text
             </span>
             <span>
              |
             </span>
             <span>
              #text
             </span>
            </p>
            <div>
             <div>
              <strong>
               #text
              </strong>
             </div>
             <div>
              <span>
               Rate this
              </span>
              <div>
               <div>
                <span>
                 1 2 3 4 5 6 7 8 9 10
                </span>
                <span>
                 <span>
                  #text
                 </span>
                 (
                 <span>
                  10
                 </span>
                 ) +
                </span>
                <span>
                 X
                </span>
               </div>
              </div>
             </div>
            </div>
            <p>
             #text
            </p>
            <p>
             Director:Stars:,,,(
             <a>
              #text
             </a>
             ) +
             <span>
              |
             </span>
             (
             <a>
              #text
             </a>
             ) +
            </p>
            <p>
             <span>
              Votes:
             </span>
             <span>
              #text
             </span>
            </p>
           </div>
          </div>"""

print(max(len(text1), len(text2)))
print(jaccard.distance(text1, text2))