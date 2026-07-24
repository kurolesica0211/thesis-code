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
Prince Friso of Orange-Nassau (Dutch: Johan Friso Bernhard Christiaan David van Oranje-Nassau van Amsberg; 25 September 1968 – 12 August 2013) was the second son of Queen Beatrix of the Netherlands and Claus von Amsberg, and younger brother of King Willem-Alexander.
On 17 February 2012, Prince Friso was buried under an avalanche in Lech, Austria, while skiing off piste.
On 12 August 2013, one and a half years after the accident, Prince Friso died from complications.
Early life and education

Johan Friso Bernhard Christiaan David was born on 25 September 1968 at the Academic Hospital Utrecht (now the University Medical Center Utrecht) in Utrecht, Netherlands.
He was the second son of Princess Beatrix and Prince Claus, and grandson of Queen Juliana of the Netherlands and Prince Bernhard.
He had one older brother, current King Willem-Alexander of the Netherlands (b. 1967), and one younger brother, Prince Constantijn (b. 1969).
His titles at birth were Prince of the Netherlands, Prince of Orange-Nassau, and Jonkheer van Amsberg.
Prince Friso was baptized on 28 December 1968 in the Dom Church in Utrecht.
His godparents were Prince Harald of Norway, Johan Christian Baron von Jenisch, Herman van Roijen, Queen Juliana of the Netherlands and Christina von Amsberg.
Work

Prince Friso worked from 1995 to 1996 at the Amsterdam branch of the international management consultancy McKinsey.
After completing an MBA-programme at INSEAD, Prince Friso worked from 1998 to 2003 as a vice president at Goldman Sachs International in London.
From October 2006, Prince Friso was managing director in the London office of a private investment and advisory firm, Wolfensohn & Company.
Prince Friso was a co-founder of the MRI Centre in Amsterdam and was also a founding shareholder of Wizzair, the largest low-cost airline in Eastern Europe.
He was honorary chairman of the Prince Claus Fund for Culture and Development (a position he held together with his younger brother, Prince Constantijn).
Prior to his accident, Prince Friso was working as a chief financial officer for URENCO, a uranium enrichment company.
Marriage and children

On 30 June 2003, it was announced that Prince Friso was to marry Mabel Wisse Smit.
The Dutch cabinet, however, did not seek permission from parliament for this marriage, a constitutional requirement if Prince Friso was to remain a member of the Dutch Royal House and in line of succession for the throne; at the time, he was second in line after his older brother, Willem-Alexander.
The Prime Minister Jan Peter Balkenende explained that this was due to discussions with Mabel Wisse Smit in October 2003, when she had admitted that her previous statements about an alleged relationship with Klaas Bruinsma (1953–1991), a known Dutch drug baron, had not been complete and accurate.
They nevertheless married at Oude Kerk (Delft) on 24 April 2004, and Mabel Wisse Smit became a member of the Dutch Royal Family but not a member of the Dutch Royal House.
Considering that his elder brother King Willem-Alexander has three daughters, Prince Friso's exclusion from the succession was unlikely to have an effect on the monarchy in the Netherlands.
After their marriage, Prince Friso and his wife Princess Mabel set up home in London, in the suburb of Kew.
The couple's first daughter, Countess Emma Luana Ninette Sophie of Orange-Nassau, Jonkvrouwe van Amsberg, was born on 26 March 2005 in London.
Their second daughter, Countess Joanna Zaria Nicoline Milou of Orange-Nassau, Jonkvrouwe van Amsberg, was born on 18 June 2006, also in London.
Avalanche accident

Accident

On 17 February 2012, Prince Friso was buried under an avalanche in Lech, Austria, and he was taken to a hospital in Innsbruck.
According to a formal statement of the Netherlands Government Information Service (RVD), a prognosis could be given only after some days.
The prince's condition was described as "stable, but critical".
Resulting complications

The Dutch Royal Family issued a statement on 19 February saying "The Royal Family is very grateful and deeply touched by all expressions of support and sympathy after the ski accident of His Royal Highness Prince Friso.
On 24 February, an Innsbruck medical team announced that the prince had been buried for 25 minutes, followed by a 50-minute CPR to treat his cardiac arrest.
It remained unclear whether the prince would ever regain full consciousness.
Koller said that the Prince's family might now look for a rehabilitation institution.
On the same day the Dutch Royal Family issued a statement requesting that the privacy of the Prince's family be respected to enable them to come to terms with his condition.
On 1 March 2012, Prince Friso was transferred to the Wellington Hospital, in London where he and his wife had lived for many years.
On 19 November 2012, it was announced that the prince had started to show some signs of consciousness but it was still not certain whether he would ever wake up, and if he did, in what state.
On 9 July 2013, Prince Friso was moved back to Huis ten Bosch in the Netherlands.
Death and funeral

On 12 August 2013, it was announced that Prince Friso had died in Huis ten Bosch of complications from the accident.
He was buried on 16 August in the Dutch Reformed Cemetery in the hamlet of Lage Vuursche near Drakesteijn Castle, where he had spent his childhood and where Princess Beatrix returned to live in February 2014.
Titles, styles and honours

Titles and styles

Under the Act on the Membership of the Royal House (2002), Prince Friso lost the title 'Prince of the Netherlands' by entering into a marriage without an Act of Consent.
By a royal decree of 19 March 2004, Prince Friso was granted the surname 'Van Oranje-Nassau van Amsberg', the hereditary noble predicate 'Jonkheer (Jonkvrouw) van Amsberg and the hereditary title 'Count of Orange-Nassau', to take effect upon his marriage.
By the same decree, he was allowed to retain his title 'Prince of Orange-Nassau' as a personal and non-hereditary title and the style of 'Royal Highness'.
According to the notification of this Royal Decree, any children born to the couple were to receive the surname 'van Oranje-Nassau van Amsberg' and become a 'Count (Countess) of Orange-Nassau' and also have the noble predicate 'Jonkheer (Jonkvrouw) van Amsberg'.
So his children had the same titles and names as those of Prince Constantijn, and showing that they belong to the royal family descending from Queen Beatrix and Prince Claus.
Referred to from birth as Prince Johan-Friso, in 2004, the royal court announced that he had requested that he would henceforth be called "Prince Friso".
Honours

National

Ancestry

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (5a1c7c16-8ac2-42e9-b863-3fd72034e140)
 Call ID: 5a1c7c16-8ac2-42e9-b863-3fd72034e140
  Args:
    type: :Man
    source: :Prince_Friso
  AssignClass (cd80df45-d192-4cad-bc27-52c7e8e04a3d)
 Call ID: cd80df45-d192-4cad-bc27-52c7e8e04a3d
  Args:
    type: :Person
    source: :Prince_Friso
  AssignClass (cac5159e-294b-47ae-bdf2-5d868b0cf569)
 Call ID: cac5159e-294b-47ae-bdf2-5d868b0cf569
  Args:
    type: :Woman
    source: :Queen_Beatrix
  AssignClass (74fe777b-aa6b-4123-8b3b-b30546c20839)
 Call ID: 74fe777b-aa6b-4123-8b3b-b30546c20839
  Args:
    type: :Person
    source: :Queen_Beatrix
  AssignClass (c46b959e-6abf-49b7-80df-bc8945df6eb9)
 Call ID: c46b959e-6abf-49b7-80df-bc8945df6eb9
  Args:
    type: :Man
    source: :Claus_von_Amsberg
  AssignClass (300b6a01-9a65-414e-8667-9713b8fafc56)
 Call ID: 300b6a01-9a65-414e-8667-9713b8fafc56
  Args:
    type: :Person
    source: :Claus_von_Amsberg
  AssignClass (5378dc81-0f67-4304-85b2-28cfafc97d3b)
 Call ID: 5378dc81-0f67-4304-85b2-28cfafc97d3b
  Args:
    type: :Man
    source: :King_Willem-Alexander
  AssignClass (33078d7b-4e5b-44bf-b23b-1afa2fce45f5)
 Call ID: 33078d7b-4e5b-44bf-b23b-1afa2fce45f5
  Args:
    type: :Person
    source: :King_Willem-Alexander
  AssignClass (11f81725-23e3-458c-aeee-9a05ac57cf05)
 Call ID: 11f81725-23e3-458c-aeee-9a05ac57cf05
  Args:
    type: :Man
    source: :Prince_Constantijn
  AssignClass (3d251fc9-0500-4952-adcd-4dc81bfc27f0)
 Call ID: 3d251fc9-0500-4952-adcd-4dc81bfc27f0
  Args:
    type: :Person
    source: :Prince_Constantijn
  AssignClass (7ff3c196-da0a-4ede-8905-403f84f1f7c7)
 Call ID: 7ff3c196-da0a-4ede-8905-403f84f1f7c7
  Args:
    type: :Woman
    source: :Queen_Juliana
  AssignClass (d3fe1737-78f5-4592-8758-3f14b897b834)
 Call ID: d3fe1737-78f5-4592-8758-3f14b897b834
  Args:
    type: :Person
    source: :Queen_Juliana
  AssignClass (024768c9-8b92-4814-8f58-1e6f97322720)
 Call ID: 024768c9-8b92-4814-8f58-1e6f97322720
  Args:
    type: :Man
    source: :Prince_Bernhard
  AssignClass (43506545-c03d-4ac3-aa06-ae259c188b98)
 Call ID: 43506545-c03d-4ac3-aa06-ae259c188b98
  Args:
    type: :Person
    source: :Prince_Bernhard
  AssignClass (b6fc6269-bcf5-4c79-9b6d-e482f82a4718)
 Call ID: b6fc6269-bcf5-4c79-9b6d-e482f82a4718
  Args:
    type: :Woman
    source: :Mabel_Wisse_Smit
  AssignClass (b3c9e3d3-ac0a-4e17-b224-57489f3abd29)
 Call ID: b3c9e3d3-ac0a-4e17-b224-57489f3abd29
  Args:
    type: :Person
    source: :Mabel_Wisse_Smit
  AssignClass (e2881d11-f48b-49f4-992f-b821f906d7ea)
 Call ID: e2881d11-f48b-49f4-992f-b821f906d7ea
  Args:
    type: :Woman
    source: :Countess_Emma_Luana_Ninette_Sophie
  AssignClass (2bf693e7-7b81-483a-a76b-e0354038707c)
 Call ID: 2bf693e7-7b81-483a-a76b-e0354038707c
  Args:
    type: :Person
    source: :Countess_Emma_Luana_Ninette_Sophie
  AssignClass (575d866d-9cb1-40e3-87de-9400ea03a514)
 Call ID: 575d866d-9cb1-40e3-87de-9400ea03a514
  Args:
    type: :Woman
    source: :Countess_Joanna_Zaria_Nicoline_Milou
  AssignClass (e9f6b27f-57c3-4315-a4ec-cbd369c5bd9c)
 Call ID: e9f6b27f-57c3-4315-a4ec-cbd369c5bd9c
  Args:
    type: :Person
    source: :Countess_Joanna_Zaria_Nicoline_Milou
  AddLiteral (5346c221-a1d0-44b8-b4fa-4ed2c1a72e80)
 Call ID: 5346c221-a1d0-44b8-b4fa-4ed2c1a72e80
  Args:
    relation: :hasBirthYear
    literal_value: 1968
    literal_type: xsd:integer
    source: :Prince_Friso
  AddLiteral (3283133e-456d-4e7c-b570-1e70932eb8e2)
 Call ID: 3283133e-456d-4e7c-b570-1e70932eb8e2
  Args:
    source: :Prince_Friso
    literal_type: xsd:integer
    literal_value: 2013
    relation: :hasDeathYear
  AddTriple (ee466445-70d2-4260-bb27-cf9681cf9e70)
 Call ID: ee466445-70d2-4260-bb27-cf9681cf9e70
  Args:
    relation: :hasFather
    target: :Claus_von_Amsberg
    source: :Prince_Friso
  AddTriple (65799a40-9c18-4e5e-bf11-2289ee2ea4c4)
 Call ID: 65799a40-9c18-4e5e-bf11-2289ee2ea4c4
  Args:
    relation: :hasMother
    target: :Queen_Beatrix
    source: :Prince_Friso
  AddTriple (190a1587-65dd-4ce8-94af-ba2292925987)
 Call ID: 190a1587-65dd-4ce8-94af-ba2292925987
  Args:
    target: :King_Willem-Alexander
    source: :Prince_Friso
    relation: :isBrotherOf
  AddTriple (a3e0421b-d6e8-42c4-a912-0277bdafbba1)
 Call ID: a3e0421b-d6e8-42c4-a912-0277bdafbba1
  Args:
    target: :Prince_Constantijn
    source: :Prince_Friso
    relation: :isBrotherOf
  AddTriple (f835adf7-3a41-481d-b402-d24c227397c6)
 Call ID: f835adf7-3a41-481d-b402-d24c227397c6
  Args:
    relation: :isChildOf
    target: :Queen_Juliana
    source: :Prince_Friso
  AddTriple (aeb8a80b-252e-4217-9711-e11134394481)
 Call ID: aeb8a80b-252e-4217-9711-e11134394481
  Args:
    relation: :isChildOf
    target: :Prince_Bernhard
    source: :Prince_Friso
  AddTriple (d8333cb5-088a-4b56-83e9-49bce0148278)
 Call ID: d8333cb5-088a-4b56-83e9-49bce0148278
  Args:
    source: :Prince_Friso
    target: :Countess_Emma_Luana_Ninette_Sophie
    relation: :hasChild
  AddTriple (5e702482-2705-4bee-8215-b8d183e8ae1b)
 Call ID: 5e702482-2705-4bee-8215-b8d183e8ae1b
  Args:
    relation: :hasChild
    source: :Prince_Friso
    target: :Countess_Joanna_Zaria_Nicoline_Milou
  AddLiteral (86834c41-0998-4a6a-897d-dddd2e7f4438)
 Call ID: 86834c41-0998-4a6a-897d-dddd2e7f4438
  Args:
    source: :Prince_Friso
    literal_type: xsd:integer
    literal_value: 2004
    relation: :hasMarriageYear
  AddTriple (d479b559-72fa-40ab-98ba-e3feae41f309)
 Call ID: d479b559-72fa-40ab-98ba-e3feae41f309
  Args:
    target: :Mabel_Wisse_Smit
    source: :Prince_Friso
    relation: :hasRelation
  Finish (acf8f28d-0914-4be1-a4f9-ab23a4a93f93)
 Call ID: acf8f28d-0914-4be1-a4f9-ab23a4a93f93
  Args: