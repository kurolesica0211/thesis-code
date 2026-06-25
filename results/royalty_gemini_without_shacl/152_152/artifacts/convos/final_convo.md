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
  AssignClass (36900173-7c7f-48af-8905-a6b09af651c8)
 Call ID: 36900173-7c7f-48af-8905-a6b09af651c8
  Args:
    source: Mary_Princess_Royal
    type: :Woman
  AssignClass (3162595e-7bed-4b03-ab86-a9b0f6cb3dab)
 Call ID: 3162595e-7bed-4b03-ab86-a9b0f6cb3dab
  Args:
    source: Mary_Princess_Royal
    type: :Person
  AddLiteral (e17ba459-7578-49f7-b8bb-2cf3a2401d1f)
 Call ID: e17ba459-7578-49f7-b8bb-2cf3a2401d1f
  Args:
    source: Mary_Princess_Royal
    literal_value: 1897
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (e04de381-c415-4e05-a99d-6730d9278196)
 Call ID: e04de381-c415-4e05-a99d-6730d9278196
  Args:
    literal_value: 1965
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Mary_Princess_Royal
  AddLiteral (ca829376-60d4-465c-866e-15e0d5df6fde)
 Call ID: ca829376-60d4-465c-866e-15e0d5df6fde
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Mary
    source: Mary_Princess_Royal
  AssignClass (b811f761-1814-4faa-8230-9ec984ec2f35)
 Call ID: b811f761-1814-4faa-8230-9ec984ec2f35
  Args:
    source: King_George_V
    type: :Man
  AssignClass (775cdae6-3c2e-4007-98eb-8db91f49e669)
 Call ID: 775cdae6-3c2e-4007-98eb-8db91f49e669
  Args:
    type: :Person
    source: King_George_V
  AssignClass (955c9e9d-030c-4e13-8d7e-2c68a37dc64f)
 Call ID: 955c9e9d-030c-4e13-8d7e-2c68a37dc64f
  Args:
    type: :Woman
    source: Queen_Mary
  AssignClass (0e403736-c8bc-439a-81c2-81e2f847e352)
 Call ID: 0e403736-c8bc-439a-81c2-81e2f847e352
  Args:
    source: Queen_Mary
    type: :Person
  AddTriple (941dd9e1-9366-4864-b518-18f2903af92e)
 Call ID: 941dd9e1-9366-4864-b518-18f2903af92e
  Args:
    source: Mary_Princess_Royal
    relation: :hasFather
    target: King_George_V
  AddTriple (f8a420ab-96e1-4da9-8dc1-9d764593d494)
 Call ID: f8a420ab-96e1-4da9-8dc1-9d764593d494
  Args:
    source: Mary_Princess_Royal
    relation: :hasMother
    target: Queen_Mary
  AssignClass (b4c2856f-9a5e-4bbb-9950-e32f6e250004)
 Call ID: b4c2856f-9a5e-4bbb-9950-e32f6e250004
  Args:
    type: :Man
    source: Edward_VIII
  AssignClass (2768efe6-57a5-4d25-a12d-451f502fe79c)
 Call ID: 2768efe6-57a5-4d25-a12d-451f502fe79c
  Args:
    type: :Person
    source: Edward_VIII
  AssignClass (f1022ed5-0f89-4688-8295-02c71ad2b3eb)
 Call ID: f1022ed5-0f89-4688-8295-02c71ad2b3eb
  Args:
    source: George_VI
    type: :Man
  AssignClass (df2cc52d-0f71-4017-9f73-d4d9e4c375fa)
 Call ID: df2cc52d-0f71-4017-9f73-d4d9e4c375fa
  Args:
    type: :Person
    source: George_VI
  AddTriple (56fa0088-2ce2-4e30-ac25-3374c634a8ce)
 Call ID: 56fa0088-2ce2-4e30-ac25-3374c634a8ce
  Args:
    source: Mary_Princess_Royal
    target: Edward_VIII
    relation: :hasBrother
  AddTriple (514f361a-d9c8-4baf-9557-ee464e8cb5a7)
 Call ID: 514f361a-d9c8-4baf-9557-ee464e8cb5a7
  Args:
    source: Mary_Princess_Royal
    target: George_VI
    relation: :hasBrother
  AssignClass (04218fb6-0452-4e83-b240-c36f05454060)
 Call ID: 04218fb6-0452-4e83-b240-c36f05454060
  Args:
    source: Henry_Lascelles
    type: :Man
  AssignClass (7a5c9445-f899-4995-8c5b-2c404c8a7f64)
 Call ID: 7a5c9445-f899-4995-8c5b-2c404c8a7f64
  Args:
    type: :Person
    source: Henry_Lascelles
  AddLiteral (262100fd-1f12-4137-a08d-ae446fca505b)
 Call ID: 262100fd-1f12-4137-a08d-ae446fca505b
  Args:
    literal_type: xsd:integer
    literal_value: 1922
    relation: :hasMarriageYear
    source: Mary_Princess_Royal
  AddTriple (6572c62b-6d87-41d7-9501-2c8290aa3b35)
 Call ID: 6572c62b-6d87-41d7-9501-2c8290aa3b35
  Args:
    source: Mary_Princess_Royal
    relation: :hasRelation
    target: Henry_Lascelles
  AssignClass (17894fac-93af-4f26-9fed-a8a2b65629c9)
 Call ID: 17894fac-93af-4f26-9fed-a8a2b65629c9
  Args:
    source: George_Lascelles
    type: :Man
  AssignClass (3e9049c9-4302-4217-9549-14ef8541507e)
 Call ID: 3e9049c9-4302-4217-9549-14ef8541507e
  Args:
    source: George_Lascelles
    type: :Person
  AssignClass (fbf346fc-b439-4488-b030-a66c69e9b508)
 Call ID: fbf346fc-b439-4488-b030-a66c69e9b508
  Args:
    type: :Man
    source: Gerald_David_Lascelles
  AssignClass (3b5f32b7-177b-4315-a8ad-c37d99a8ace1)
 Call ID: 3b5f32b7-177b-4315-a8ad-c37d99a8ace1
  Args:
    type: :Person
    source: Gerald_David_Lascelles
  AddTriple (84b78394-cdb1-464a-81f5-1421a0121c1e)
 Call ID: 84b78394-cdb1-464a-81f5-1421a0121c1e
  Args:
    source: Mary_Princess_Royal
    relation: :hasSon
    target: George_Lascelles
  AddTriple (e420355b-ad08-4c55-b2e0-13fe2c72da5d)
 Call ID: e420355b-ad08-4c55-b2e0-13fe2c72da5d
  Args:
    source: Mary_Princess_Royal
    target: Gerald_David_Lascelles
    relation: :hasSon
  Finish (49dcbc53-93b7-4262-a47b-ecc3a33e2a00)
 Call ID: 49dcbc53-93b7-4262-a47b-ecc3a33e2a00
  Args: