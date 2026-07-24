================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Mary, Princess Royal (Victoria Alexandra Alice Mary; 25 April 1897 – 28 March 1965), was a member of the British royal family.
She was the only daughter of King George V and Queen Mary, the sister of kings Edward VIII and George VI, and the aunt of Queen Elizabeth II.
In 1922, she married Henry Lascelles, Viscount Lascelles (later the 6th Earl of Harewood), and they had two sons, George Lascelles, 7th Earl of Harewood, and Gerald David Lascelles.
Mary was granted the title Princess Royal in 1932.
Early life and education

Mary was born at 3:30 pm on 25 April 1897 at York Cottage on the Sandringham Estate in Norfolk, during the reign of her great-grandmother Queen Victoria.
She was the third child and only daughter of the Duke and Duchess of York, later King George V and Queen Mary.
Her father was the only surviving son of the Prince and Princess of Wales, later King Edward VII and Queen Alexandra, and her mother was the eldest child and only daughter of the Duke and Duchess of Teck.
She was named Victoria Alexandra Alice Mary after her paternal great-grandmother Queen Victoria; her paternal grandmother, Alexandra, Princess of Wales; her maternal grandmother, Mary Adelaide, Duchess of Teck; and her great-aunt, Alice, Grand Duchess of Hesse and by Rhine, with whom she shared a birthday.
She was known by the last of her given names, Mary.
At the time of her birth she was fifth in the line of succession to the British throne after her grandfather, father, and elder brothers Edward (later Edward VIII) and Albert (later George VI), and moved down the line following the births of her younger brothers Henry, George, and John.
She was baptised at St Mary Magdalene's Church near Sandringham on 7 June by William Dalrymple Maclagan, Archbishop of York.
Her godparents were the Queen (her great-grandmother), the King of the Hellenes (her paternal great-uncle), the Dowager Empress of Russia (her paternal great-aunt), the Prince and Princess of Wales (her paternal grandparents), the Duchess of Teck (her maternal grandmother), Princess Victoria of Wales (her paternal aunt), and Prince Francis of Teck (her maternal uncle).
Her grandfather succeeded to the throne in 1901 when Mary was three years old.
Mary was educated by governesses, although she shared some lessons with her brothers Edward, Albert, and Henry.
Charity work

During World War I, Mary visited hospitals and welfare organisations with her mother, assisting with schemes that provided comfort to British servicemen and support to their families.
One such initiative was Princess Mary's Christmas Gift Fund, through which gifts worth £100,000 were distributed to serving soldiers and sailors for Christmas 1914, the equivalent of £9.55 million in 2023.
In 1918, she was appointed colonel-in-chief of the Royal Scots, an honour bestowed by her father, the King.
On 20 November 1918, she became the first member of the royal family to visit France following the Armistice.
While visiting Ypres she recognised two soldiers from the Royal Scots; the regiment was stationed nearby, and a march‐past of its 17th battalion was arranged.
Mary's public duties reflected her interest in nursing, the Girl Guide movement, and the Women's Services.
In the period leading up to her marriage, girls and women across the British Empire named Mary or its variants (including Marie, May, and Miriam) formed "The Marys of the Empire," and contributed to a wedding present fund.
In July 2013, it was reported that British Pathé had identified newsreel film from 1927 showing the ancestors of Catherine Middleton, as Lord Mayors of Leeds, hosting Mary at the Young Women's Christian Association in Hunslet.
In 1921, Mary became the first patron of the Not Forgotten Association, a role she held until her death in 1965.
In the 1920s, Mary was a patron of the Leeds Triennial Musical Festival.
By the 1940s, she was attending opening nights and many of the festival's performances, as was her son, George, and his wife, the Countess of Harewood, née Marion Stein, a former concert pianist.
George was a noted music critic whose career included serving as artistic director of the Leeds Triennial Musical Festival.
In 1931, Mary was appointed patron of the Yorkshire Ladies Council of Education.
In July 1927, it was reported that, at a garden party at Headingley Cricket Ground, Mary was served tea alongside dignitaries who included members of the Middleton family; Olive Middleton, great-grandmother of Catherine, Princess of Wales, was among them.
Mary and her son, George, were patrons of the Yorkshire Symphony Orchestra which performed soirées at their home, Harewood House.
Among those attending was the orchestra's co-founder, Richard Noël Middleton, who was on friendly terms with Mary.
Middleton's wife, Olive, served on Mary's fundraising committee for the Leeds General Infirmary.
The committee's vice-presidents included Mary's sister-in-law, the Hon.
Mrs Edward Lascelles, who served alongside Olive and her relative Jessie Beatrice Kitson.
In 1936, Mary became patron of the Leeds Infirmary.
Marriage and family

On 28 February 1922, Mary married Henry, Viscount Lascelles, the elder son of the 5th Earl of Harewood and his wife, Lady Florence Bridgeman, daughter of the 3rd Earl of Bradford of Weston Park.
Mary was 24 years old, while the groom was 39.
The ceremony was the first royal wedding to be covered in fashion magazines, including Vogue.
Mary's gown was designed by Messrs Raville and featured emblems of Britain and India.
It was also the first royal occasion in which Lady Elizabeth Bowes-Lyon, a friend of Mary, participated as one of the bridesmaids.
She later married Mary's brother, Albert, and became queen consort of the United Kingdom upon his accession in 1936.
Mary and Henry had two sons:


Family homes and interests

Mary and her husband had homes in London (first Chesterfield House in South Audley Street, and later 32 Green Street, Mayfair) and in Yorkshire (first Goldsborough Hall, and later Harewood House).
London

Prior to their marriage, Henry had purchased a palatial London townhouse, Chesterfield House in South Audley Street, for £140,000.
In 1931, King George V and Queen Mary purchased 32 Green Street, Mayfair, as a London home for their daughter, rendering Chesterfield House surplus to the couple's needs.
Mary and Henry vacated Chesterfield House in early 1932.
Queen Mary reportedly expressed an interest in purchasing 32 Green Street as a London home for her daughter in 1931, and consent was obtained from the property's owner, Hugh Grosvenor, 2nd Duke of Westminster, with the proviso that the Grosvenor Estates could maintain the right to repurchase the house at a future date if its use as a royal residence ceased.
Following the outbreak World War II, Mary was granted the use of a grace‐and‐favour apartment at St James's Palace, which remained her official London residence for the rest of her life.
While at Goldsborough Hall, Mary commissioned internal alterations by the architect Sydney Kitson to suit the upbringing of her two children, and she instigated the development of formal beech‐hedge‐lined borders extending from the south terrace for a quarter of a mile down an avenue of lime trees.
The limes were planted by her relatives as they visited the hall throughout the 1920s, including her father, King George, and her mother, Queen Mary.
After becoming Countess of Harewood upon the death of her father‐in‐law, Mary moved to Harewood House and took a keen interest in the interior decoration and renovation of the Lascelles family seat.
In farming pursuits, she became an expert in cattle breeding and served on the board of trustees of the Royal Agricultural Society of England, of which her husband had been president.
In December 2012, some of Mary's belongings were sold in "Harewood: Collecting in the Royal Tradition", an auction organised by Christie's.
In the first half of the 20th century, Mary occasionally rode with the Bramham Moor Hunt – Henry was Master of the Hunt – and she entertained many horse-racing enthusiasts at Harewood house parties for the race meetings at Wetherby and York.
Princess Royal

On 6 October 1929, Henry succeeded his father as 6th Earl of Harewood, having previously been created a Knight of the Garter upon his marriage.
On 1 January 1932, George V declared that Mary should bear the title Princess Royal, succeeding her aunt Princess Louise, Duchess of Fife, who had died a year earlier.
Mary was particularly close to her eldest brother, the Prince of Wales, known as David to his family, who became Edward VIII upon the death of their father in 1936.
After the abdication crisis, Mary and Henry went to stay with the former Edward VIII, by then created Duke of Windsor, at Enzesfeld Castle near Vienna.
Later, in November 1947, she allegedly declined to attend the wedding of her niece, Princess Elizabeth, to Lieutenant Philip Mountbatten as the Duke of Windsor had not been invited.
She posed for photographs with them before she and the duke boarded the ship on which they travelled to visit their ailing mother, Queen Mary.
At the outbreak of World War II, Mary became chief controller and later controller commandant of the Auxiliary Territorial Service, renamed the Women's Royal Army Corps in 1949.
After the death in 1942 of her younger brother, the Duke of Kent, she became president of Papworth Hospital.
Mary became air chief commandant of Princess Mary's Royal Air Force Nursing Service in 1950, and received the honorary rank of general in the British Army in 1956.
Also, in 1949, the 10th Gurkha Rifles were renamed the 10th Princess Mary's Own Gurkha Rifles in her honour.
After Henry's death in 1947, Mary lived at Harewood House with her elder son and his family.
She attended the coronation of Queen Elizabeth II in June 1953, and later represented the Queen at the independence celebrations of Trinidad and Tobago in 1962, and Zambia in 1964.
Mary visited her brother, the Duke of Windsor, at the London Clinic in March 1965, while he recovered from recent eye surgery.
Death and legacy

Mary suffered a fatal heart attack on 28 March 1965 during a walk with her elder son, George, and his children in the grounds of the Harewood House estate.
She was buried next to Henry in the Lascelles family vault at All Saints' Church, Harewood, after a private family funeral at York Minster.
Six British monarchs reigned during Mary's lifetime: Victoria (her great-grandmother), Edward VII (her grandfather), George V (her father), Edward VIII and George VI (her brothers), and Elizabeth II (her niece).
She is typically remembered as an uncontroversial figure within the royal family.
Mary was portrayed by Kate Phillips in Downton Abbey (2019).
During the British Mandate of Palestine, a major street in Jerusalem next to the Old City was called Princess Mary Street.
Titles, styles, honours and arms

Titles and styles

Mary was known as Princess Mary of York at birth.
Mary was not styled Her Royal Highness from birth, only gaining that style in 1898 by letters patent granted by her great-grandmother, Queen Victoria.
After Victoria's death in January 1901, Mary was known as Princess Mary of Cornwall and York, until her father's creation as Prince of Wales in November of that year, when she assumed the title Princess Mary of Wales.
Upon her father's accession as George V in 1910, Mary assumed the style of "Her Royal Highness The Princess Mary".
In 1922, Mary married Henry, Viscount Lascelles and began using the title "Her Royal Highness The Princess Mary, Viscountess Lascelles".
When her husband succeeded as Earl of Harewood in 1929, Mary became known as "Her Royal Highness The Princess Mary, Countess of Harewood".
In 1932, her father granted her the title Princess Royal, which had previously belonged to her aunt Louise until her death the year before.
For the rest of her life, Mary was known as "Her Royal Highness The Princess Royal".
Honours

British, British Empire and Commonwealth

Foreign

Freedom of the City

Academic

Memberships

Honorary military appointments

British

Military ranks

Arms

In 1931, Mary was awarded her own personal arms, being the royal arms, differenced by a label argent of three points, each bearing a cross gules.
}} Media related to Mary, Princess Royal and Countess of Harewood at Wikimedia Commons



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns1:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a883d779-cf7c-43af-8311-69678fcf738f)
 Call ID: a883d779-cf7c-43af-8311-69678fcf738f
  Args:
    type: :Woman
    source: :Mary_Princess_Royal
  AddLiteral (c2aa7227-54fc-439d-ad3f-23786ff83b6b)
 Call ID: c2aa7227-54fc-439d-ad3f-23786ff83b6b
  Args:
    literal_value: 1897
    relation: :hasBirthYear
    source: :Mary_Princess_Royal
    literal_type: xsd:integer
  AddLiteral (34d3b188-1d06-47de-be26-ff9f3f711fa1)
 Call ID: 34d3b188-1d06-47de-be26-ff9f3f711fa1
  Args:
    literal_type: xsd:integer
    source: :Mary_Princess_Royal
    relation: :hasDeathYear
    literal_value: 1965
  AssignClass (d6ff3090-0a61-4216-8b1f-e210a34c92e9)
 Call ID: d6ff3090-0a61-4216-8b1f-e210a34c92e9
  Args:
    type: :Man
    source: :King_George_V
  AssignClass (dfa8513e-c7ac-4a9a-a632-a0052093953d)
 Call ID: dfa8513e-c7ac-4a9a-a632-a0052093953d
  Args:
    type: :Woman
    source: :Queen_Mary
  AddTriple (3e12b9db-4eaf-4e49-9aca-cf4d2af8978d)
 Call ID: 3e12b9db-4eaf-4e49-9aca-cf4d2af8978d
  Args:
    relation: :isFatherOf
    source: :King_George_V
    target: :Mary_Princess_Royal
  AddTriple (80f470c8-639d-4a35-b10d-e86acd051ae0)
 Call ID: 80f470c8-639d-4a35-b10d-e86acd051ae0
  Args:
    source: :Queen_Mary
    relation: :isMotherOf
    target: :Mary_Princess_Royal
  AssignClass (cc923e64-af9a-4687-85a1-0907a3c37104)
 Call ID: cc923e64-af9a-4687-85a1-0907a3c37104
  Args:
    type: :Man
    source: :Edward_VIII
  AssignClass (575cab1b-b0a7-4367-9b9f-d1951590236d)
 Call ID: 575cab1b-b0a7-4367-9b9f-d1951590236d
  Args:
    type: :Man
    source: :George_VI
  AddTriple (50f979bd-cbc7-4e4e-a78d-0f960cf331cc)
 Call ID: 50f979bd-cbc7-4e4e-a78d-0f960cf331cc
  Args:
    source: :Edward_VIII
    relation: :isBrotherOf
    target: :Mary_Princess_Royal
  AddTriple (d8f773c9-a407-4079-8e2a-14775e9f266a)
 Call ID: d8f773c9-a407-4079-8e2a-14775e9f266a
  Args:
    source: :George_VI
    relation: :isBrotherOf
    target: :Mary_Princess_Royal
  AssignClass (2cfe521b-040e-4980-b468-8e016149f299)
 Call ID: 2cfe521b-040e-4980-b468-8e016149f299
  Args:
    type: :Woman
    source: :Queen_Elizabeth_II
  AddTriple (132e21df-d9e5-4370-b4a4-b77dc6890426)
 Call ID: 132e21df-d9e5-4370-b4a4-b77dc6890426
  Args:
    target: :Queen_Elizabeth_II
    source: :Mary_Princess_Royal
    relation: :isAuntOf
  AssignClass (180a3bd2-9bfc-4137-ac5d-f394896aea4f)
 Call ID: 180a3bd2-9bfc-4137-ac5d-f394896aea4f
  Args:
    type: :Man
    source: :Henry_Lascelles_6th_Earl_of_Harewood
  AddLiteral (415e5a30-23cd-42fc-bbbc-83bd93ba91ee)
 Call ID: 415e5a30-23cd-42fc-bbbc-83bd93ba91ee
  Args:
    literal_value: 1922
    source: :Mary_Princess_Royal
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (fe2e53fb-10b4-4f29-b608-ba003dcc5e8b)
 Call ID: fe2e53fb-10b4-4f29-b608-ba003dcc5e8b
  Args:
    relation: :hasRelation
    source: :Mary_Princess_Royal
    target: :Henry_Lascelles_6th_Earl_of_Harewood
  AssignClass (b00b630e-45d3-4485-b54c-bc6d96dbdc36)
 Call ID: b00b630e-45d3-4485-b54c-bc6d96dbdc36
  Args:
    type: :Man
    source: :George_Lascelles_7th_Earl_of_Harewood
  AssignClass (e359092a-78de-446f-8b12-85d7ff1db804)
 Call ID: e359092a-78de-446f-8b12-85d7ff1db804
  Args:
    type: :Man
    source: :Gerald_David_Lascelles
  AddTriple (5eb6fa93-09b4-4c75-b473-7be8d36a25dc)
 Call ID: 5eb6fa93-09b4-4c75-b473-7be8d36a25dc
  Args:
    target: :George_Lascelles_7th_Earl_of_Harewood
    source: :Mary_Princess_Royal
    relation: :isMotherOf
  AddTriple (77a25312-fc08-48b9-8d7a-d295b6c812eb)
 Call ID: 77a25312-fc08-48b9-8d7a-d295b6c812eb
  Args:
    target: :Gerald_David_Lascelles
    relation: :isMotherOf
    source: :Mary_Princess_Royal
  AddTriple (d8ae28bd-079b-4800-9f09-60b4e0c6e937)
 Call ID: d8ae28bd-079b-4800-9f09-60b4e0c6e937
  Args:
    target: :George_Lascelles_7th_Earl_of_Harewood
    source: :Henry_Lascelles_6th_Earl_of_Harewood
    relation: :isFatherOf
  AddTriple (4bd8b419-d51a-489c-acfb-3a123664fadc)
 Call ID: 4bd8b419-d51a-489c-acfb-3a123664fadc
  Args:
    target: :Gerald_David_Lascelles
    relation: :isFatherOf
    source: :Henry_Lascelles_6th_Earl_of_Harewood
  Finish (5e7e1232-a42e-47bf-9997-af5ad238c138)
 Call ID: 5e7e1232-a42e-47bf-9997-af5ad238c138
  Args: