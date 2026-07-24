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
Ernst August, Hereditary Prince of Hanover (German:
Ernst August Prinz von Hannover Herzog zu Braunschweig und Lüneburg, Königlicher Prinz von Großbritannien und Irland; born 19 July 1983) is a German financier and the eldest child of Ernst August, Prince of Hanover (head of the ancient House of Hanover which once ruled the Kingdom of Hanover and were rulers of Great Britain until 1901) and his first wife Chantal Hochuli.
Due to his father's second marriage, he is also the stepson of Caroline, Princess of Hanover, a Monegasque Princess and the sister of Albert II of Monaco.
Background

Ernst August and his younger brother Christian were born in Hildesheim, Lower Saxony, while their half-sister, Alexandra, was born in Austria and lives with her mother in Monaco.
Ernst August was baptized on 15 October 1983 at Marienburg Castle, his godparents including Felipe VI of Spain and Constantine II of Greece.
Until his mid-teens, Ernst August and his brother lived at Hurlingham Lodge in London.
He also descends from Germany's last emperor, Wilhelm II, following whose abdication at the end of World War I the Hanovers also lost sovereignty over the Duchy of Brunswick, while retaining much of their continental personal property.
Education

Ernst August began his secondary education at Malvern College, but ultimately completed that phase of his education with an International Baccalaureate back on the Continent.
After his marriage in 2017 he and his wife moved to Hanover.
Already in 2004, his father had signed over to him the German property of the House of Hanover, including gothic-revival Marienburg Castle, the agricultural estates of Calenberg Castle and the Fürstenhaus ("Princely House") at Herrenhausen Gardens in Hanover; the elaborate museum in this small palace, built by King George I of Great Britain in 1720, has been closed to the public since 2011.
Since 2004, the prince has taken over many representative tasks on behalf of his father.
The father remained in charge of the Austrian family assets until 2013 when he was removed from the chairmanship of a family foundation based in Liechtenstein, the Duke of Cumberland Foundation, which holds the properties near Gmunden in Austria, the Hanovers' main residence in exile after 1866 when their Kingdom of Hanover was annexed by Prussia.
Instead, the younger Ernst August was put in charge, reportedly for negligence on part of his father, at the initiative of the foundation's trustee Prince Michael of Liechtenstein.
In 2017 Ernst August the Elder filed legal action to recover chairmanship.
In 2014, Ernst August lent a number of paintings and objects for a Lower Saxony state exhibition, When the Royals came from Hanover - The rulers of Hanover on England's throne, which included exhibits in five museums and castles under the auspices of Charles, Prince of Wales.
Thirty of more than 1000 items were contributed by Elizabeth II, including the State Crown of George I, while Ernst August provided the king's famous Augsburg silver throne and other furniture dating to 1720.
He hosted a parallel exhibition, The Way to the Crown, at Marienburg Castle until through 2016, displaying—among other items—the crown jewels of the Kingdom of Hanover.
Marriage and issue

In the summer of 2016 Ernst August became engaged to Ekaterina Igorievna Malysheva (born 30 July 1986, Apatity, Soviet Russia), a Russian designer, general manager of Audiotube and founder of EKAT, and daughter of Igor Malyshev and Svetlana Malysheva.
Days before the wedding, his father, the elder Ernst August publicly stated concerns about potential adverse impacts on family assets if the younger Ernst August were to marry his chosen fiancée.
Despite the dynastic tradition of obtaining the head of the House of Hanover's express, prior authorization for an heir's marriage in accordance with an 1836 Hanoverian house law (as Ernst August's father had done when marrying his sons' future mother in 1981), the bridegroom's father declared his intention to withhold consent for his son's marriage to Ekaterina Malysheva, reportedly in a dispute over family assets.
Nonetheless, the civil marriage took place on 6 July 2017 in Hanover's New Town Hall and was conducted by the mayor of Hanover, Stefan Schostok.
The church marriage took place on 8 July 2017 in the Hanover Market Church at which the former Landesbischof of the Evangelical-Lutheran Church of Hanover, Horst Hirschler, presided.
Her wedding dress was the work of Lebanese designer Sandra Mansour, and she wore a tiara that belonged to the former Kaiser Wilhelm II's only daughter, Princess Victoria Louise of Prussia.
Among the wedding guests were: Prince Christian of Hanover, Princess Alexandra of Hanover, Andrea Casiraghi, Tatiana Santo Domingo, Pierre Casiraghi, Beatrice Borromeo, Charlotte Casiraghi, Georg Friedrich, Prince of Prussia and his wife Princess Sophie, Crown Prince Pavlos of Greece and his wife Crown Princess Marie-Chantal, Hereditary Prince Hubertus of Saxe-Coburg and Gotha, Alexander, Prince of Schaumburg-Lippe and Princess Elisabeth von Thurn und Taxis.
The father of the groom, Prince Ernst August, did not attend the wedding.
Thus, while descendants of non-dynastic marriages may have a legal right to the use of "Prinz/Prinzessin von Hannover Herzog/Herzogin zu Braunschweig und Lüneburg Königlicher Prinz/Prinzessin von Großbritannien und Irland" as surnames, they are not recognized as bearing rank, styles titles or membership appertaining to the House of Hanover, according to its house rules.
Nor is the title "Prince/ss of Great Britain and Ireland", re-claimed by the deposed House of Hanover in 1931, accorded by British sovereigns to members thereof born after 30 November 1917.


Notes and references

External links



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
  AssignClass (61fcc392-4032-4c62-82dc-2cb5b359b51c)
 Call ID: 61fcc392-4032-4c62-82dc-2cb5b359b51c
  Args:
    type: :Man
    source: Ernst_August_Hereditary_Prince_of_Hanover
  AssignClass (45dd18bd-687d-42ae-9021-4fe986377371)
 Call ID: 45dd18bd-687d-42ae-9021-4fe986377371
  Args:
    source: Ernst_August_Prince_of_Hanover
    type: :Man
  AssignClass (b3784653-39a3-4f3e-ad10-b23201780c22)
 Call ID: b3784653-39a3-4f3e-ad10-b23201780c22
  Args:
    type: :Woman
    source: Chantal_Hochuli
  AssignClass (f76094a9-84a1-43e9-b839-b99d62290222)
 Call ID: f76094a9-84a1-43e9-b839-b99d62290222
  Args:
    type: :Man
    source: Christian_of_Hanover
  AssignClass (258056b2-9dd2-4352-8076-eed0907e95a1)
 Call ID: 258056b2-9dd2-4352-8076-eed0907e95a1
  Args:
    source: Alexandra_of_Hanover
    type: :Woman
  AssignClass (d9c472c6-f078-455a-be5b-ed1e10ece45a)
 Call ID: d9c472c6-f078-455a-be5b-ed1e10ece45a
  Args:
    type: :Woman
    source: Ekaterina_Igorievna_Malysheva
  AssignClass (eb2d82be-b021-4564-a1bf-e5207a5b831e)
 Call ID: eb2d82be-b021-4564-a1bf-e5207a5b831e
  Args:
    source: Igor_Malyshev
    type: :Man
  AssignClass (7ecbe7f9-99df-43f8-ae16-0465d8cf7284)
 Call ID: 7ecbe7f9-99df-43f8-ae16-0465d8cf7284
  Args:
    type: :Woman
    source: Svetlana_Malysheva
  AddLiteral (e4c5f921-ec57-4ae7-8799-58d88b4a7731)
 Call ID: e4c5f921-ec57-4ae7-8799-58d88b4a7731
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Ernst_August_Hereditary_Prince_of_Hanover
    literal_value: 1983
  AddTriple (4c612602-037d-4347-93c3-4d79b07f0e4f)
 Call ID: 4c612602-037d-4347-93c3-4d79b07f0e4f
  Args:
    relation: :hasFather
    target: Ernst_August_Prince_of_Hanover
    source: Ernst_August_Hereditary_Prince_of_Hanover
  AddTriple (029922c9-5930-484a-9019-be0667393769)
 Call ID: 029922c9-5930-484a-9019-be0667393769
  Args:
    source: Ernst_August_Hereditary_Prince_of_Hanover
    relation: :hasMother
    target: Chantal_Hochuli
  AddTriple (06e3f179-bf35-4253-9bcc-59bd327d4630)
 Call ID: 06e3f179-bf35-4253-9bcc-59bd327d4630
  Args:
    source: Christian_of_Hanover
    relation: :isBrotherOf
    target: Ernst_August_Hereditary_Prince_of_Hanover
  AddTriple (842bf57b-b6dd-44b6-93e3-cabb0e93263e)
 Call ID: 842bf57b-b6dd-44b6-93e3-cabb0e93263e
  Args:
    source: Christian_of_Hanover
    target: Ernst_August_Prince_of_Hanover
    relation: :hasFather
  AddTriple (9ef36026-944a-4de2-bb91-6a95ba105097)
 Call ID: 9ef36026-944a-4de2-bb91-6a95ba105097
  Args:
    relation: :hasMother
    target: Chantal_Hochuli
    source: Christian_of_Hanover
  AddTriple (4ecc83dc-9ad3-4712-af53-bbf66eca2521)
 Call ID: 4ecc83dc-9ad3-4712-af53-bbf66eca2521
  Args:
    source: Alexandra_of_Hanover
    relation: :isSisterOf
    target: Ernst_August_Hereditary_Prince_of_Hanover
  AddTriple (8364f735-aa38-48ad-99b6-7e534fc6bb60)
 Call ID: 8364f735-aa38-48ad-99b6-7e534fc6bb60
  Args:
    source: Alexandra_of_Hanover
    target: Ernst_August_Prince_of_Hanover
    relation: :hasFather
  AddLiteral (e37a9c88-05d0-48b1-afad-9eaa2999eb78)
 Call ID: e37a9c88-05d0-48b1-afad-9eaa2999eb78
  Args:
    relation: :hasBirthYear
    source: Ekaterina_Igorievna_Malysheva
    literal_value: 1986
    literal_type: xsd:integer
  AddTriple (bf1d0a4e-d85a-4590-9e90-9420333235d6)
 Call ID: bf1d0a4e-d85a-4590-9e90-9420333235d6
  Args:
    relation: :hasFather
    target: Igor_Malyshev
    source: Ekaterina_Igorievna_Malysheva
  AddTriple (6634e433-d184-43e8-886c-a84ddb48ea46)
 Call ID: 6634e433-d184-43e8-886c-a84ddb48ea46
  Args:
    source: Ekaterina_Igorievna_Malysheva
    target: Svetlana_Malysheva
    relation: :hasMother
  AddLiteral (d822e15a-910e-4ac7-a65b-b6d3a14470c5)
 Call ID: d822e15a-910e-4ac7-a65b-b6d3a14470c5
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Ernst_August_Hereditary_Prince_of_Hanover
    literal_value: 2017
  AddTriple (4e518572-5796-47ae-a208-2e55f7cdb0e7)
 Call ID: 4e518572-5796-47ae-a208-2e55f7cdb0e7
  Args:
    source: Ernst_August_Hereditary_Prince_of_Hanover
    relation: :hasRelation
    target: Ekaterina_Igorievna_Malysheva
  Finish (d0784e4e-cf52-4347-9d7d-5b588add0b6b)
 Call ID: d0784e4e-cf52-4347-9d7d-5b588add0b6b
  Args: