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
  AssignClass (56325c10-3326-4bd8-8ab0-42e0077d1a39)
 Call ID: 56325c10-3326-4bd8-8ab0-42e0077d1a39
  Args:
    source: :PrinceFriso
    type: :Man
  AssignClass (ade718d9-d557-4bdf-b431-09710313901a)
 Call ID: ade718d9-d557-4bdf-b431-09710313901a
  Args:
    source: :PrinceFriso
    type: :Person
  AssignClass (60c08005-a08e-4d24-b34a-e49c09fe033e)
 Call ID: 60c08005-a08e-4d24-b34a-e49c09fe033e
  Args:
    source: :QueenBeatrix
    type: :Woman
  AssignClass (265ccab3-d1a0-4e7d-9c59-89576b2b9145)
 Call ID: 265ccab3-d1a0-4e7d-9c59-89576b2b9145
  Args:
    type: :Person
    source: :QueenBeatrix
  AssignClass (e9eddeac-a23f-441b-a96a-e6fef8fff622)
 Call ID: e9eddeac-a23f-441b-a96a-e6fef8fff622
  Args:
    source: :ClausVonAmsberg
    type: :Man
  AssignClass (38419452-e817-48b7-969a-8197e2f8ca5b)
 Call ID: 38419452-e817-48b7-969a-8197e2f8ca5b
  Args:
    type: :Person
    source: :ClausVonAmsberg
  AssignClass (c81f63e7-257a-45e7-b754-8a0fd4f3030d)
 Call ID: c81f63e7-257a-45e7-b754-8a0fd4f3030d
  Args:
    source: :KingWillemAlexander
    type: :Man
  AssignClass (0c422711-6326-4041-862c-72c1efa4b0c5)
 Call ID: 0c422711-6326-4041-862c-72c1efa4b0c5
  Args:
    type: :Person
    source: :KingWillemAlexander
  AssignClass (d1a15d8d-007b-4caa-afcc-bebfafeec7be)
 Call ID: d1a15d8d-007b-4caa-afcc-bebfafeec7be
  Args:
    source: :PrinceConstantijn
    type: :Man
  AssignClass (a92eaa5e-a4d7-46d5-ad63-d98050320c62)
 Call ID: a92eaa5e-a4d7-46d5-ad63-d98050320c62
  Args:
    type: :Person
    source: :PrinceConstantijn
  AssignClass (a4df00e7-c856-41ea-83ee-e7addd50ee7b)
 Call ID: a4df00e7-c856-41ea-83ee-e7addd50ee7b
  Args:
    type: :Woman
    source: :QueenJuliana
  AssignClass (4dc32d63-5d31-4485-8bef-ff432bf306d3)
 Call ID: 4dc32d63-5d31-4485-8bef-ff432bf306d3
  Args:
    type: :Person
    source: :QueenJuliana
  AssignClass (f660a73a-583d-462e-8333-e1e8582d81bc)
 Call ID: f660a73a-583d-462e-8333-e1e8582d81bc
  Args:
    source: :PrinceBernhard
    type: :Man
  AssignClass (f9c62819-7003-44f0-95c7-7887244894d7)
 Call ID: f9c62819-7003-44f0-95c7-7887244894d7
  Args:
    type: :Person
    source: :PrinceBernhard
  AssignClass (1a3a600c-f644-4859-802e-338ce3e74182)
 Call ID: 1a3a600c-f644-4859-802e-338ce3e74182
  Args:
    type: :Woman
    source: :MabelWisseSmit
  AssignClass (9a8fd6df-e678-4e39-b6dc-1153e16e6cbc)
 Call ID: 9a8fd6df-e678-4e39-b6dc-1153e16e6cbc
  Args:
    source: :MabelWisseSmit
    type: :Person
  AssignClass (fede67ec-fa3f-460d-9b35-b1c7123aeabd)
 Call ID: fede67ec-fa3f-460d-9b35-b1c7123aeabd
  Args:
    type: :Woman
    source: :CountessEmmaLuana
  AssignClass (3a79147c-bbd9-4e12-8837-ee102324ae90)
 Call ID: 3a79147c-bbd9-4e12-8837-ee102324ae90
  Args:
    type: :Person
    source: :CountessEmmaLuana
  AssignClass (5d9e9ba6-9602-40ed-8ec7-731f39ee85f2)
 Call ID: 5d9e9ba6-9602-40ed-8ec7-731f39ee85f2
  Args:
    type: :Woman
    source: :CountessJoannaZaria
  AssignClass (b238b440-8068-41b2-adc1-ad87e20c99f4)
 Call ID: b238b440-8068-41b2-adc1-ad87e20c99f4
  Args:
    source: :CountessJoannaZaria
    type: :Person
  AddLiteral (3d039cd1-4eae-4baf-9478-04d5fb989660)
 Call ID: 3d039cd1-4eae-4baf-9478-04d5fb989660
  Args:
    source: :PrinceFriso
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1968
  AddLiteral (c3641be7-534f-4945-a667-4ebee7ee9433)
 Call ID: c3641be7-534f-4945-a667-4ebee7ee9433
  Args:
    literal_value: 2013
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: :PrinceFriso
  AddLiteral (08f82e66-d873-4e6a-a65b-ca07ba47c4b1)
 Call ID: 08f82e66-d873-4e6a-a65b-ca07ba47c4b1
  Args:
    source: :KingWillemAlexander
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1967
  AddLiteral (a8702201-e60d-4da8-8bdd-6492120c0855)
 Call ID: a8702201-e60d-4da8-8bdd-6492120c0855
  Args:
    literal_type: xsd:integer
    source: :PrinceConstantijn
    literal_value: 1969
    relation: :hasBirthYear
  AddLiteral (0f8ab2c2-9d2d-46ac-85ce-fb267546bad4)
 Call ID: 0f8ab2c2-9d2d-46ac-85ce-fb267546bad4
  Args:
    literal_value: 2004
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :PrinceFriso
  AddTriple (0b32bf8d-2a4c-48a6-b26e-849575dba484)
 Call ID: 0b32bf8d-2a4c-48a6-b26e-849575dba484
  Args:
    source: :PrinceFriso
    target: :ClausVonAmsberg
    relation: :hasFather
  AddTriple (f61e94c5-243b-4055-a95e-408c2f286e38)
 Call ID: f61e94c5-243b-4055-a95e-408c2f286e38
  Args:
    relation: :hasMother
    target: :QueenBeatrix
    source: :PrinceFriso
  AddTriple (c0f6a176-b1ed-4c8e-9731-695300715c1f)
 Call ID: c0f6a176-b1ed-4c8e-9731-695300715c1f
  Args:
    source: :PrinceFriso
    relation: :isBrotherOf
    target: :KingWillemAlexander
  AddTriple (a3083b7a-da35-440b-9bd2-f25f4945db6e)
 Call ID: a3083b7a-da35-440b-9bd2-f25f4945db6e
  Args:
    relation: :isBrotherOf
    target: :PrinceConstantijn
    source: :PrinceFriso
  AddTriple (6a0c7414-70e8-463b-9cd0-b3327b3ec63e)
 Call ID: 6a0c7414-70e8-463b-9cd0-b3327b3ec63e
  Args:
    source: :QueenBeatrix
    relation: :hasMother
    target: :QueenJuliana
  AddTriple (075dc3d3-724e-4f4c-baa9-10fa9565792a)
 Call ID: 075dc3d3-724e-4f4c-baa9-10fa9565792a
  Args:
    target: :PrinceBernhard
    relation: :hasFather
    source: :QueenBeatrix
  AddTriple (3aeed749-30f1-4413-9b4d-2280b113b838)
 Call ID: 3aeed749-30f1-4413-9b4d-2280b113b838
  Args:
    source: :PrinceFriso
    relation: :hasFather
    target: :PrinceBernhard
  AddTriple (d200c855-53ff-4469-8c6c-981e5b96a5b5)
 Call ID: d200c855-53ff-4469-8c6c-981e5b96a5b5
  Args:
    relation: :hasMother
    target: :QueenJuliana
    source: :PrinceFriso
  AddTriple (1227e71e-9c4d-44c1-a7f4-0119214be14c)
 Call ID: 1227e71e-9c4d-44c1-a7f4-0119214be14c
  Args:
    relation: :hasParent
    target: :CountessEmmaLuana
    source: :MabelWisseSmit
  AddTriple (a7e1ff70-1f32-47c0-9a77-33be0f960367)
 Call ID: a7e1ff70-1f32-47c0-9a77-33be0f960367
  Args:
    relation: :hasParent
    target: :CountessJoannaZaria
    source: :MabelWisseSmit
  AddTriple (735eb5ce-42df-4c11-babd-e25e71e3ac42)
 Call ID: 735eb5ce-42df-4c11-babd-e25e71e3ac42
  Args:
    source: :PrinceFriso
    relation: :hasParent
    target: :CountessEmmaLuana
  AddTriple (7b7e24f4-5a35-4e74-9ac4-e91d06d978df)
 Call ID: 7b7e24f4-5a35-4e74-9ac4-e91d06d978df
  Args:
    target: :CountessJoannaZaria
    relation: :hasParent
    source: :PrinceFriso
  Finish (2db3cbb9-36c2-435e-886e-912ce9a4cdee)
 Call ID: 2db3cbb9-36c2-435e-886e-912ce9a4cdee
  Args: