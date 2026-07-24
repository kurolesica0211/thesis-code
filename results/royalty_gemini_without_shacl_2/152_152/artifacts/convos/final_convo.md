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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b5eddb63-31cc-40aa-8514-eceb3959ba9c)
 Call ID: b5eddb63-31cc-40aa-8514-eceb3959ba9c
  Args:
    type: :Woman
    source: Mary_Princess_Royal
  AddLiteral (432c3ac2-4377-4604-bbdb-d56f68b6ff37)
 Call ID: 432c3ac2-4377-4604-bbdb-d56f68b6ff37
  Args:
    source: Mary_Princess_Royal
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1897
  AddLiteral (10e2fc64-70bb-47be-aac0-7cd9416a952c)
 Call ID: 10e2fc64-70bb-47be-aac0-7cd9416a952c
  Args:
    literal_type: xsd:integer
    literal_value: 1965
    relation: :hasDeathYear
    source: Mary_Princess_Royal
  AssignClass (06642a1e-f3b4-48f5-b541-8692d55cd444)
 Call ID: 06642a1e-f3b4-48f5-b541-8692d55cd444
  Args:
    type: :Man
    source: George_V
  AssignClass (d67b6ce9-e33f-4747-a52a-8ff09f2ce5e3)
 Call ID: d67b6ce9-e33f-4747-a52a-8ff09f2ce5e3
  Args:
    type: :Woman
    source: Queen_Mary
  AddTriple (39815eea-adf0-42f0-9d29-aae190612cae)
 Call ID: 39815eea-adf0-42f0-9d29-aae190612cae
  Args:
    source: Mary_Princess_Royal
    relation: :hasFather
    target: George_V
  AddTriple (034dd102-1147-4d96-bc25-428db84bc88d)
 Call ID: 034dd102-1147-4d96-bc25-428db84bc88d
  Args:
    source: Mary_Princess_Royal
    target: Queen_Mary
    relation: :hasMother
  AssignClass (e000065d-483f-4574-bdc0-d98822e46b45)
 Call ID: e000065d-483f-4574-bdc0-d98822e46b45
  Args:
    type: :Man
    source: Edward_VIII
  AssignClass (8f7c297a-cf99-42aa-8030-fc0f9464c923)
 Call ID: 8f7c297a-cf99-42aa-8030-fc0f9464c923
  Args:
    type: :Man
    source: George_VI
  AddTriple (14a230f4-f36e-48cd-9723-71302de41383)
 Call ID: 14a230f4-f36e-48cd-9723-71302de41383
  Args:
    relation: :hasBrother
    target: Edward_VIII
    source: Mary_Princess_Royal
  AddTriple (3087980a-d664-4f25-b8bb-ffce9981e714)
 Call ID: 3087980a-d664-4f25-b8bb-ffce9981e714
  Args:
    target: George_VI
    relation: :hasBrother
    source: Mary_Princess_Royal
  AssignClass (f776d25c-a06c-424a-98c8-63e5dc726410)
 Call ID: f776d25c-a06c-424a-98c8-63e5dc726410
  Args:
    type: :Woman
    source: Elizabeth_II
  AddTriple (50478362-e9e4-46c3-b360-78c1576c84fd)
 Call ID: 50478362-e9e4-46c3-b360-78c1576c84fd
  Args:
    target: Elizabeth_II
    relation: :isAuntOf
    source: Mary_Princess_Royal
  AssignClass (7d245ad1-6d48-479b-8fc0-d377db3e806b)
 Call ID: 7d245ad1-6d48-479b-8fc0-d377db3e806b
  Args:
    type: :Man
    source: Henry_Lascelles
  AddLiteral (83617118-4b0b-46b3-b030-2086ccb959e9)
 Call ID: 83617118-4b0b-46b3-b030-2086ccb959e9
  Args:
    source: Mary_Princess_Royal
    relation: :hasMarriageYear
    literal_value: 1922
    literal_type: xsd:integer
  AddTriple (ab9e5f1d-07bd-4555-b312-afed66d85d29)
 Call ID: ab9e5f1d-07bd-4555-b312-afed66d85d29
  Args:
    relation: :hasRelation
    target: Henry_Lascelles
    source: Mary_Princess_Royal
  AssignClass (cdebca44-eff2-4bf5-a7bf-d81ee68a81e2)
 Call ID: cdebca44-eff2-4bf5-a7bf-d81ee68a81e2
  Args:
    type: :Man
    source: George_Lascelles
  AssignClass (c096dcb3-5037-4c64-a9c8-4d7e9c2681a1)
 Call ID: c096dcb3-5037-4c64-a9c8-4d7e9c2681a1
  Args:
    type: :Man
    source: Gerald_David_Lascelles
  AddTriple (51fc18dc-8f3d-4bdd-bc09-3034b25d09d5)
 Call ID: 51fc18dc-8f3d-4bdd-bc09-3034b25d09d5
  Args:
    source: Mary_Princess_Royal
    relation: :hasSon
    target: George_Lascelles
  AddTriple (f36eb678-d028-4cd0-9b67-7c2858a77068)
 Call ID: f36eb678-d028-4cd0-9b67-7c2858a77068
  Args:
    relation: :hasSon
    target: Gerald_David_Lascelles
    source: Mary_Princess_Royal
  AddTriple (a145f120-2274-4457-a1e3-5efffeea5518)
 Call ID: a145f120-2274-4457-a1e3-5efffeea5518
  Args:
    source: George_Lascelles
    relation: :hasFather
    target: Henry_Lascelles
  AddTriple (9ff8bebb-8a5b-47d0-8350-983ca9eba7b5)
 Call ID: 9ff8bebb-8a5b-47d0-8350-983ca9eba7b5
  Args:
    target: Henry_Lascelles
    relation: :hasFather
    source: Gerald_David_Lascelles
  Finish (0ace8d1f-7265-4382-bc68-ace8691073d0)
 Call ID: 0ace8d1f-7265-4382-bc68-ace8691073d0
  Args: