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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (f6a61ae9-cae5-4baf-a593-0d1baf8de5ca)
 Call ID: f6a61ae9-cae5-4baf-a593-0d1baf8de5ca
  Args:
    source: ErnstAugust_HereditaryPrinceOfHanover
    type: :Man
  AssignClass (a4400a92-3d69-498d-ae6c-3d6cda540f00)
 Call ID: a4400a92-3d69-498d-ae6c-3d6cda540f00
  Args:
    source: ErnstAugust_PrinceOfHanover
    type: :Man
  AssignClass (5fb9f617-4b4f-49d7-9ceb-8b771c291b37)
 Call ID: 5fb9f617-4b4f-49d7-9ceb-8b771c291b37
  Args:
    type: :Woman
    source: ChantalHochuli
  AssignClass (fec7fd2b-b74d-40d0-b503-8642dbb1ddba)
 Call ID: fec7fd2b-b74d-40d0-b503-8642dbb1ddba
  Args:
    type: :Man
    source: ChristianOfHanover
  AssignClass (5dc5a6fc-3ade-44c7-bf23-c0de5e6cae40)
 Call ID: 5dc5a6fc-3ade-44c7-bf23-c0de5e6cae40
  Args:
    type: :Woman
    source: AlexandraOfHanover
  AssignClass (ec677dbf-1dc1-4cdc-8a19-ec9370f23d26)
 Call ID: ec677dbf-1dc1-4cdc-8a19-ec9370f23d26
  Args:
    type: :Woman
    source: EkaterinaIgorievnaMalysheva
  AssignClass (00007625-54ef-44c7-aed1-cda74491d70d)
 Call ID: 00007625-54ef-44c7-aed1-cda74491d70d
  Args:
    source: IgorMalyshev
    type: :Man
  AssignClass (5ad80e38-0efc-4fca-be2d-63b0d0fce528)
 Call ID: 5ad80e38-0efc-4fca-be2d-63b0d0fce528
  Args:
    type: :Woman
    source: SvetlanaMalysheva
  AddLiteral (a9ed685b-6a55-4d43-8d6c-49f97d43b636)
 Call ID: a9ed685b-6a55-4d43-8d6c-49f97d43b636
  Args:
    source: ErnstAugust_HereditaryPrinceOfHanover
    literal_value: 1983
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (6c97ecf2-72cb-41c0-987e-c666e24e19ee)
 Call ID: 6c97ecf2-72cb-41c0-987e-c666e24e19ee
  Args:
    source: ErnstAugust_HereditaryPrinceOfHanover
    target: ErnstAugust_PrinceOfHanover
    relation: :hasFather
  AddTriple (7ef9e6f1-9699-41a2-95fc-8ed45e53fc69)
 Call ID: 7ef9e6f1-9699-41a2-95fc-8ed45e53fc69
  Args:
    source: ErnstAugust_HereditaryPrinceOfHanover
    target: ChantalHochuli
    relation: :hasMother
  AddTriple (f4c999c5-cdfb-41af-ba56-9540b2693a31)
 Call ID: f4c999c5-cdfb-41af-ba56-9540b2693a31
  Args:
    relation: :hasBrother
    source: ErnstAugust_HereditaryPrinceOfHanover
    target: ChristianOfHanover
  AddTriple (50ba878c-7371-4ef7-839c-daabede4abd6)
 Call ID: 50ba878c-7371-4ef7-839c-daabede4abd6
  Args:
    target: ErnstAugust_PrinceOfHanover
    source: ChristianOfHanover
    relation: :hasFather
  AddTriple (89c561c5-3786-425a-b6dc-baf6f5e8dc21)
 Call ID: 89c561c5-3786-425a-b6dc-baf6f5e8dc21
  Args:
    source: ChristianOfHanover
    target: ChantalHochuli
    relation: :hasMother
  AddTriple (cc3db428-f89d-4ff6-929a-1da1525c41c4)
 Call ID: cc3db428-f89d-4ff6-929a-1da1525c41c4
  Args:
    relation: :hasFather
    target: ErnstAugust_PrinceOfHanover
    source: AlexandraOfHanover
  AddLiteral (34d39c44-60f3-4010-a53c-6a28812dfb50)
 Call ID: 34d39c44-60f3-4010-a53c-6a28812dfb50
  Args:
    source: EkaterinaIgorievnaMalysheva
    literal_value: 1986
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (bea81ab5-8bd4-44a8-8ce0-2cba84978bd2)
 Call ID: bea81ab5-8bd4-44a8-8ce0-2cba84978bd2
  Args:
    source: EkaterinaIgorievnaMalysheva
    target: IgorMalyshev
    relation: :hasFather
  AddTriple (59a87af6-c2e6-4ff2-80fe-60567cbb6ed4)
 Call ID: 59a87af6-c2e6-4ff2-80fe-60567cbb6ed4
  Args:
    source: EkaterinaIgorievnaMalysheva
    target: SvetlanaMalysheva
    relation: :hasMother
  AddLiteral (0c4311a1-5acc-4710-b65d-52768faf8fcb)
 Call ID: 0c4311a1-5acc-4710-b65d-52768faf8fcb
  Args:
    source: ErnstAugust_HereditaryPrinceOfHanover
    literal_value: 2017
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (0650da61-0c6f-4682-8f52-554436a0c0a0)
 Call ID: 0650da61-0c6f-4682-8f52-554436a0c0a0
  Args: