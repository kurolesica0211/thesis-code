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
  AssignClass (b71f21e3-2ac6-4d6a-8496-d668a74f2f60)
 Call ID: b71f21e3-2ac6-4d6a-8496-d668a74f2f60
  Args:
    type: :Man
    source: :PrinceGeorgeOfWales
  AssignClass (4537c433-406c-431c-8fd0-4a425b447307)
 Call ID: 4537c433-406c-431c-8fd0-4a425b447307
  Args:
    type: :Person
    source: :PrinceGeorgeOfWales
  AddLiteral (0b98570b-6544-497e-80d0-82d60cef38b7)
 Call ID: 0b98570b-6544-497e-80d0-82d60cef38b7
  Args:
    literal_value: 2013
    source: :PrinceGeorgeOfWales
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (88266453-a3d9-4433-86c6-1317e77e38a9)
 Call ID: 88266453-a3d9-4433-86c6-1317e77e38a9
  Args:
    type: :Man
    source: :WilliamPrinceOfWales
  AssignClass (b80ff63a-fae9-4a4e-8d4d-c6fa6e0254fd)
 Call ID: b80ff63a-fae9-4a4e-8d4d-c6fa6e0254fd
  Args:
    source: :WilliamPrinceOfWales
    type: :Person
  AssignClass (96b5bbcc-5f87-4286-a0d1-874d650cbf20)
 Call ID: 96b5bbcc-5f87-4286-a0d1-874d650cbf20
  Args:
    type: :Woman
    source: :CatherinePrincessOfWales
  AssignClass (91a2cd2b-a85c-4b13-a375-d140f631e9bb)
 Call ID: 91a2cd2b-a85c-4b13-a375-d140f631e9bb
  Args:
    type: :Person
    source: :CatherinePrincessOfWales
  AddTriple (45eca0de-ca21-4c74-ace4-7c8256f3ec59)
 Call ID: 45eca0de-ca21-4c74-ace4-7c8256f3ec59
  Args:
    source: :PrinceGeorgeOfWales
    target: :WilliamPrinceOfWales
    relation: :hasFather
  AddTriple (043ae4d6-3d9c-464e-b2cc-f4d80c7fa884)
 Call ID: 043ae4d6-3d9c-464e-b2cc-f4d80c7fa884
  Args:
    source: :PrinceGeorgeOfWales
    relation: :hasMother
    target: :CatherinePrincessOfWales
  AssignClass (016dfd86-deb5-40e9-ad3c-eb07b86f869e)
 Call ID: 016dfd86-deb5-40e9-ad3c-eb07b86f869e
  Args:
    type: :Man
    source: :KingCharlesIII
  AssignClass (10ef9c1f-3d62-4737-9355-284363f0c82a)
 Call ID: 10ef9c1f-3d62-4737-9355-284363f0c82a
  Args:
    type: :Person
    source: :KingCharlesIII
  AssignClass (49224b7c-886e-4e0f-8621-8540312f566c)
 Call ID: 49224b7c-886e-4e0f-8621-8540312f566c
  Args:
    source: :DianaPrincessOfWales
    type: :Woman
  AssignClass (02ecaf3a-0135-42fe-91ac-302e16e7b9c9)
 Call ID: 02ecaf3a-0135-42fe-91ac-302e16e7b9c9
  Args:
    type: :Person
    source: :DianaPrincessOfWales
  AddTriple (5899cd48-15c1-4f67-98d0-48b4d23f4bef)
 Call ID: 5899cd48-15c1-4f67-98d0-48b4d23f4bef
  Args:
    source: :WilliamPrinceOfWales
    relation: :hasFather
    target: :KingCharlesIII
  AddTriple (7891ac95-0357-4342-a758-f245253a095c)
 Call ID: 7891ac95-0357-4342-a758-f245253a095c
  Args:
    source: :WilliamPrinceOfWales
    relation: :hasMother
    target: :DianaPrincessOfWales
  AssignClass (d89f9bd2-abb6-44f1-bbec-3792873c9dab)
 Call ID: d89f9bd2-abb6-44f1-bbec-3792873c9dab
  Args:
    type: :Woman
    source: :QueenElizabethII
  AssignClass (28e69aee-ef7c-420b-a789-0e9fc6913c33)
 Call ID: 28e69aee-ef7c-420b-a789-0e9fc6913c33
  Args:
    source: :QueenElizabethII
    type: :Person
  AddTriple (838e6a6e-01d3-4f8e-a73a-2a248aed600f)
 Call ID: 838e6a6e-01d3-4f8e-a73a-2a248aed600f
  Args:
    source: :KingCharlesIII
    relation: :hasMother
    target: :QueenElizabethII
  AssignClass (6df51f7d-defa-4a6c-99b2-8fb6956cfcb0)
 Call ID: 6df51f7d-defa-4a6c-99b2-8fb6956cfcb0
  Args:
    type: :Woman
    source: :PrincessCharlotte
  AssignClass (e8ee2056-9ad4-48b6-a7e0-555c2200d3e1)
 Call ID: e8ee2056-9ad4-48b6-a7e0-555c2200d3e1
  Args:
    source: :PrincessCharlotte
    type: :Person
  AssignClass (e97a5717-d72a-4a71-b6b2-4411a3747424)
 Call ID: e97a5717-d72a-4a71-b6b2-4411a3747424
  Args:
    type: :Man
    source: :PrinceLouis
  AssignClass (f55ae5d8-34b8-4991-b709-420dc4815663)
 Call ID: f55ae5d8-34b8-4991-b709-420dc4815663
  Args:
    source: :PrinceLouis
    type: :Person
  AddTriple (e16d7231-92ac-44dc-ad0e-117ba8303759)
 Call ID: e16d7231-92ac-44dc-ad0e-117ba8303759
  Args:
    source: :PrinceGeorgeOfWales
    relation: :isSiblingOf
    target: :PrincessCharlotte
  AddTriple (6e161616-8a94-4d64-b8bf-dde026294195)
 Call ID: 6e161616-8a94-4d64-b8bf-dde026294195
  Args:
    source: :PrinceGeorgeOfWales
    target: :PrinceLouis
    relation: :isSiblingOf
  Finish (f389f71d-a513-4ed3-919b-40981684813b)
 Call ID: f389f71d-a513-4ed3-919b-40981684813b
  Args: