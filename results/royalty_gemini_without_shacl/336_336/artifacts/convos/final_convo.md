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
Count Christian of Rosenborg  (Christian Frederik Franz Knud Harald Carl Oluf Gustav Georg Erik; 22 October 1942 – 21 May 2013) was a member of the Danish royal family.
Born Prince Christian of Denmark, from 1947 he was third in the line of line of succession until the constitution was changed in 1953 to allow females to inherit the crown, placing his branch of the dynasty behind that of his cousin Margrethe and her two younger sisters.
Family

He was born at Sorgenfri Palace, Sorgenfri, as the younger son of Hereditary Prince Knud by his wife and first cousin, Princess Caroline-Mathilde of Denmark.
Loss of place in succession

From the death of his grandfather in 1947, Christian stood only behind his father and elder brother Prince Ingolf in the order of hereditary succession to the throne, with only future children of Ingolf possibly taking a place ahead of him.
His father Prince Knud was then the heir presumptive, due to succeed Christian's uncle King Frederik IX, who had three daughters but no sons.
In 1953, the Constitution of Denmark was amended to allow cognatic primogeniture.
The new law made thirteen-year-old Princess Margrethe the new heir presumptive, placing her and her two sisters before Prince Knud and his family in the succession.
Christian was thus relegated to sixth in the line of succession to the Danish throne, but more importantly, he then ranked behind Margrethe and others who were likely to have dynastic children of their own (as has, in fact, happened).
The princess became Queen Margrethe II in 1972 and reigned until her abdication in 2024.
Christian's place in the line of succession, if he had been still eligible, would have been no higher than thirteenth in 2013.
Marriage, loss of dynastic rights and children

By 1971, Princess Margrethe had produced two children, pushing Christian to 8th in the line of succession.
The king's permission to marry was not sought because it was expected to be denied, since Christian's fiancée was an untitled commoner.
Prior to his elder son's wedding in 1968, Prince Knud sought to convince his brother that Ingolf should be allowed to retain his royal title after his non-dynastic marriage, a privilege which might have been subsequently extended to Christian.
But the king refused, on the grounds that other males of the dynasty, who had been demoted to counts of Rosenborg upon marriage, might try to re-claim their royal rank if Ingolf were allowed to do so despite his marrying a commoner as they had done.
So, in 1971, Christian renounced his rights to the throne and took the title count of Rosenborg.
On 27 February 1971, at Kongens Lyngby Kirke, Kongens Lyngby, Denmark, Christian married Anne Dorte Maltoft-Nielsen (3 October 1947 in Frederikssund – 2 January 2014 in Copenhagen) who thus became Her Excellency Countess Anne Dorte of Rosenborg.
Although lacking the prior royal assent of the monarch given in the Council of State that the law required, the king expressed no personal opposition to his nephew's choice of bride and, according to Christian, the king's private consent later had to be formally registered by the King-in-Council.
In a 1985 interview with Billed-Bladet, Count Christian had explained (translated from Danish):
As protocol dictates, I had to ask my uncle, King Frederik IX, if he had any objections to my getting engaged...
I was number four in the line of succession after Princess Margrethe, Princess Benedikte, and my father.
Count Christian and Countess Anne Dorte had three daughters: 


All three were born “Komtesser” a lower title than “Grevinde” which translates to “Countess” from birth.
And a title that all daughters of Counts in Denmark are given.
Public life

Count Christian took part in some major public events associated with the royal family, in 2004, he and Countess Anne Dorte attended the wedding on 14 May 2004 of Crown Prince Frederik at Copenhagen Cathedral, Copenhagen and the subsequent reception at Fredensborg Palace.
They were included in the official guest-list as members of the Danish Royal Family when they attended the luncheon to celebrate the 75th birthday of Prince Henrik at Fredensborg Palace on 11 June 2009; and the ruby jubilee celebrations for Queen Margrethe.
Death

Count Christian died on 21 May 2013 (aged 70) at Gentofte Hospital, Copenhagen in Denmark.
A number of members of the Danish royal family, led by Queen Margrethe, attended Count Christian's funeral, held at Lyngby Church on 29 May 2013.
His wife Countess Anne Dorte of Rosenborg died just 7 months later on 2 January 2014 in Copenhagen.



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
  AssignClass (eae7cdd2-0c82-4beb-a8d6-3d4ddfb9f515)
 Call ID: eae7cdd2-0c82-4beb-a8d6-3d4ddfb9f515
  Args:
    type: :Man
    source: Christian_of_Rosenborg
  AssignClass (9d61f58e-e3e2-469c-b426-d7385d54805f)
 Call ID: 9d61f58e-e3e2-469c-b426-d7385d54805f
  Args:
    source: Christian_of_Rosenborg
    type: :Person
  AddLiteral (f79cd5fd-2a8c-44d6-aaee-9661a63b457f)
 Call ID: f79cd5fd-2a8c-44d6-aaee-9661a63b457f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1942
    source: Christian_of_Rosenborg
  AddLiteral (541bd33d-acfa-429b-b527-2596f8182355)
 Call ID: 541bd33d-acfa-429b-b527-2596f8182355
  Args:
    source: Christian_of_Rosenborg
    literal_value: 2013
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (02e6ce63-fa1a-4785-a610-5701955ea87e)
 Call ID: 02e6ce63-fa1a-4785-a610-5701955ea87e
  Args:
    type: :Man
    source: Knud_of_Denmark
  AssignClass (3c79d658-a2a6-40a5-9c65-ed8e82942f61)
 Call ID: 3c79d658-a2a6-40a5-9c65-ed8e82942f61
  Args:
    source: Knud_of_Denmark
    type: :Person
  AssignClass (33154da0-7105-4011-af16-6bc2926b1f95)
 Call ID: 33154da0-7105-4011-af16-6bc2926b1f95
  Args:
    type: :Woman
    source: Caroline-Mathilde_of_Denmark
  AssignClass (87c8fe26-fb4d-40dd-9ef4-2b62daa34365)
 Call ID: 87c8fe26-fb4d-40dd-9ef4-2b62daa34365
  Args:
    type: :Person
    source: Caroline-Mathilde_of_Denmark
  AddTriple (a7273a2b-57dc-4cbb-a7a8-6fd2fe7fa98a)
 Call ID: a7273a2b-57dc-4cbb-a7a8-6fd2fe7fa98a
  Args:
    source: Christian_of_Rosenborg
    relation: :hasFather
    target: Knud_of_Denmark
  AddTriple (1060c8a9-343b-4aa6-bdca-50d5c4964d29)
 Call ID: 1060c8a9-343b-4aa6-bdca-50d5c4964d29
  Args:
    relation: :hasMother
    target: Caroline-Mathilde_of_Denmark
    source: Christian_of_Rosenborg
  AssignClass (6ea6819c-2190-487a-b0bb-0bd1c52b36b3)
 Call ID: 6ea6819c-2190-487a-b0bb-0bd1c52b36b3
  Args:
    type: :Man
    source: Ingolf_of_Rosenborg
  AssignClass (dd3998b5-9e0e-46df-b7d7-aade9633dcdb)
 Call ID: dd3998b5-9e0e-46df-b7d7-aade9633dcdb
  Args:
    source: Ingolf_of_Rosenborg
    type: :Person
  AddTriple (3bd4614d-dee2-49a5-90e4-2f247aa3cdbe)
 Call ID: 3bd4614d-dee2-49a5-90e4-2f247aa3cdbe
  Args:
    source: Christian_of_Rosenborg
    target: Ingolf_of_Rosenborg
    relation: :hasBrother
  AssignClass (4f7580d5-502e-4d2b-bda7-e427ba4caf07)
 Call ID: 4f7580d5-502e-4d2b-bda7-e427ba4caf07
  Args:
    type: :Woman
    source: Anne_Dorte_of_Rosenborg
  AssignClass (34776288-76fa-4f27-bc22-77115ef5f08e)
 Call ID: 34776288-76fa-4f27-bc22-77115ef5f08e
  Args:
    type: :Person
    source: Anne_Dorte_of_Rosenborg
  AddLiteral (4ca90560-bf7f-4427-a75f-4045176caed1)
 Call ID: 4ca90560-bf7f-4427-a75f-4045176caed1
  Args:
    source: Christian_of_Rosenborg
    literal_value: 1971
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (d390957c-c1de-44e5-99f2-ca939f64edf2)
 Call ID: d390957c-c1de-44e5-99f2-ca939f64edf2
  Args:
    source: Christian_of_Rosenborg
    relation: :hasRelation
    target: Anne_Dorte_of_Rosenborg
  AddLiteral (4329998e-a9e1-49ad-97c0-f005d458dfe2)
 Call ID: 4329998e-a9e1-49ad-97c0-f005d458dfe2
  Args:
    literal_value: 1947
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Anne_Dorte_of_Rosenborg
  AddLiteral (bdc550fc-f3b8-4a09-888e-0c9cb1aa1c69)
 Call ID: bdc550fc-f3b8-4a09-888e-0c9cb1aa1c69
  Args:
    literal_value: 2014
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Anne_Dorte_of_Rosenborg
  Finish (3d405f51-1769-4197-b8b4-c9307ec9fb1a)
 Call ID: 3d405f51-1769-4197-b8b4-c9307ec9fb1a
  Args: