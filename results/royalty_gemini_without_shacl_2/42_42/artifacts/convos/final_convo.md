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
Prince George of Wales (George Alexander Louis; born 22 July 2013) is a member of the British royal family.
He is the eldest child of William, Prince of Wales, and Catherine, Princess of Wales, and the eldest grandchild of King Charles III and Diana, Princess of Wales.
George was born at St Mary's Hospital, London, during the reign of his paternal great-grandmother, Queen Elizabeth II, and was third in line before her death.
Infancy

George was born at 4:24 pm on 22 July 2013 at St Mary's Hospital, London, during the reign of his paternal great-grandmother, Queen Elizabeth II.
He is the eldest child of Prince William and Catherine (then known as Duke and Duchess of Cambridge).
He has a younger sister and brother, Princess Charlotte and Prince Louis.
His name was announced as George Alexander Louis on 24 July.
George was third in the line of succession to the British throne at the time of his birth.
For the first time since the reign of Queen Victoria, three generations in direct line of succession to the British throne were alive at the same time: George; his father, William; and his grandfather, Charles.
George was christened on 23 October by the archbishop of Canterbury, Justin Welby, in the Chapel Royal at St James's Palace.
Upbringing

George spent his first months in Anglesey, Wales, before his family relocated to Kensington Palace in 2014.
Although George appeared only twice, the BBC described the "nine-month-old future king" as "the star of the show".
The then Australian prime minister Tony Abbott predicted in the Parliament House, Canberra, that George would one day be welcomed there as King of Australia.
In June 2015, George made his first appearance on the balcony of Buckingham Palace following the Trooping the Colour parade.
George met Barack and Michelle Obama, then President and First Lady of the United States, in April 2016.
George started junior school under the name George Cambridge in September 2017, at Thomas's School, an independent preparatory school in Battersea.
Since September of that year, George and his siblings have attended Lambrook, an independent preparatory school in Berkshire.
George commenced flying lessons in September 2024.
George took part in his great-grandmother's Platinum Jubilee celebration in June 2022, including the Trooping the Colour carriage procession.
Elizabeth II died on 8 September 2022 and was succeeded by George's grandfather, Charles III, making George second in line to the throne behind his father.
George and his siblings occasionally accompany their parents on royal engagements, tours, and diplomatic visits.
In December 2025, George accompanied his father on a visit to The Passage, a homelessness charity of which his father is patron.
Public image

Clothing and other products used by George are often sold out, a phenomenon termed the "Prince George effect".
In August 2015, Kensington Palace stated that they wanted all global media to stop taking unauthorised photographs of George, saying that "a line  been crossed" in paparazzi methods of locating and photographing him, including surveilling the family and sending children to bring George into view.
Title and styles

George is a British prince with the official style and title "His Royal Highness Prince George of Wales".
During the reign of his great-grandmother, he was styled "His Royal Highness Prince George of Cambridge".



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
  AssignClass (e7a2b892-0bf9-4d49-bad7-fe829ddc8768)
 Call ID: e7a2b892-0bf9-4d49-bad7-fe829ddc8768
  Args:
    source: Prince_George_of_Wales
    type: :Man
  AssignClass (79982692-20ac-4a94-9fa5-01472460d185)
 Call ID: 79982692-20ac-4a94-9fa5-01472460d185
  Args:
    type: :Person
    source: Prince_George_of_Wales
  AddLiteral (4f546c20-f3ba-478a-91a8-85906da3fdb9)
 Call ID: 4f546c20-f3ba-478a-91a8-85906da3fdb9
  Args:
    relation: :hasBirthYear
    source: Prince_George_of_Wales
    literal_value: 2013
    literal_type: xsd:integer
  AddTriple (17f53f2a-b22d-4967-a56d-a2c74e5321f0)
 Call ID: 17f53f2a-b22d-4967-a56d-a2c74e5321f0
  Args:
    source: Prince_George_of_Wales
    relation: :hasFather
    target: William_Prince_of_Wales
  AddTriple (5ddd98e7-e9a6-4868-b78c-1852149d8222)
 Call ID: 5ddd98e7-e9a6-4868-b78c-1852149d8222
  Args:
    target: Catherine_Princess_of_Wales
    relation: :hasMother
    source: Prince_George_of_Wales
  AssignClass (29323cef-61dd-4ddd-8d45-961fc8885f66)
 Call ID: 29323cef-61dd-4ddd-8d45-961fc8885f66
  Args:
    type: :Man
    source: William_Prince_of_Wales
  AssignClass (4c1151f3-88ce-4f48-9430-e02fe009ba3b)
 Call ID: 4c1151f3-88ce-4f48-9430-e02fe009ba3b
  Args:
    source: William_Prince_of_Wales
    type: :Person
  AssignClass (56c9b767-b438-401a-b0ea-a66e6fc991ac)
 Call ID: 56c9b767-b438-401a-b0ea-a66e6fc991ac
  Args:
    type: :Woman
    source: Catherine_Princess_of_Wales
  AssignClass (9f8b55ba-8e96-4976-8e42-abd9b7a91fca)
 Call ID: 9f8b55ba-8e96-4976-8e42-abd9b7a91fca
  Args:
    type: :Person
    source: Catherine_Princess_of_Wales
  AddTriple (1381ea72-6691-415b-89f6-c41850d338c0)
 Call ID: 1381ea72-6691-415b-89f6-c41850d338c0
  Args:
    source: William_Prince_of_Wales
    relation: :hasFather
    target: King_Charles_III
  AddTriple (0eee8b2a-266c-4c98-9c2c-fc1c6e573c42)
 Call ID: 0eee8b2a-266c-4c98-9c2c-fc1c6e573c42
  Args:
    relation: :hasMother
    source: William_Prince_of_Wales
    target: Diana_Princess_of_Wales
  AssignClass (b6369a64-af29-4c16-b875-aba73dd8a08a)
 Call ID: b6369a64-af29-4c16-b875-aba73dd8a08a
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (000f2a63-8283-4749-9491-cfc997dcdb21)
 Call ID: 000f2a63-8283-4749-9491-cfc997dcdb21
  Args:
    type: :Person
    source: King_Charles_III
  AssignClass (cf86cafc-079f-4db7-a953-7f3c6dd6837a)
 Call ID: cf86cafc-079f-4db7-a953-7f3c6dd6837a
  Args:
    type: :Woman
    source: Diana_Princess_of_Wales
  AssignClass (b9778f06-9e9d-4f75-be92-84010a984ed5)
 Call ID: b9778f06-9e9d-4f75-be92-84010a984ed5
  Args:
    type: :Person
    source: Diana_Princess_of_Wales
  AssignClass (67d6ee76-32ce-4f90-9587-13f4b0d23f57)
 Call ID: 67d6ee76-32ce-4f90-9587-13f4b0d23f57
  Args:
    source: Princess_Charlotte
    type: :Woman
  AssignClass (7067ac60-71cd-4213-9583-c5d817898921)
 Call ID: 7067ac60-71cd-4213-9583-c5d817898921
  Args:
    source: Princess_Charlotte
    type: :Person
  AssignClass (395bbff7-d41c-453e-99fa-cd0315e172a1)
 Call ID: 395bbff7-d41c-453e-99fa-cd0315e172a1
  Args:
    type: :Man
    source: Prince_Louis
  AssignClass (52cd268a-8518-43cc-8279-34d5635a4745)
 Call ID: 52cd268a-8518-43cc-8279-34d5635a4745
  Args:
    source: Prince_Louis
    type: :Person
  AddTriple (f5e4a07b-11a5-4108-b75a-8e87f02937fc)
 Call ID: f5e4a07b-11a5-4108-b75a-8e87f02937fc
  Args:
    target: Princess_Charlotte
    relation: :isSiblingOf
    source: Prince_George_of_Wales
  AddTriple (55ce0504-31bb-4095-b94c-0ea5b65c23c2)
 Call ID: 55ce0504-31bb-4095-b94c-0ea5b65c23c2
  Args:
    target: Prince_Louis
    relation: :isSiblingOf
    source: Prince_George_of_Wales
  Finish (92c596ed-258a-47e6-8fd8-682898109f20)
 Call ID: 92c596ed-258a-47e6-8fd8-682898109f20
  Args: