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
Princess Charlotte of Wales (Charlotte Elizabeth Diana; born 2 May 2015) is a member of the British royal family.
She is the second child and only daughter of William, Prince of Wales, and Catherine, Princess of Wales, and a granddaughter of King Charles III and Diana, Princess of Wales.
Infancy

Charlotte was born at 8:34 am on 2 May 2015 at St Mary's Hospital, London, during the reign of her paternal great-grandmother, Queen Elizabeth II.
She is the second child and only daughter of Prince William and Catherine (then known as Duke and Duchess of Cambridge).
She has an older and younger brother, Prince George and Prince Louis.
On 4 May her name was announced as Charlotte Elizabeth Diana, honouring her grandfather Charles, her great-grandmother, and her grandmother Diana.
Charlotte was christened on 5 July by the archbishop of Canterbury, Justin Welby, at St Mary Magdalene Church, Sandringham.
Upbringing

The family lived at Anmer Hall in Norfolk during Charlotte's infancy, before relocating to Kensington Palace in 2017.
Charlotte started at Willcocks Nursery School in January 2018.
She joined George at Thomas's School in Battersea in September 2019, where she was known as Charlotte Cambridge.
Following the death of Elizabeth II on 8 September 2022, Charlotte's grandfather acceded to the throne as Charles III, and Charlotte became third in line to the throne.
Public image

Despite the efforts of her parents to keep their children from public view, photographs and public appearances of Charlotte continue to attract media attention.
Shopping statistics and polls among parents show that Charlotte is a major children's style icon.
Title and styles

Charlotte is a British princess with the official style and title "Her Royal Highness Princess Charlotte of Wales".
Before her father was created Prince of Wales on 9 September 2022, Charlotte was styled "Her Royal Highness Princess Charlotte of Cambridge".
Succession

Charlotte is third in the line of succession to the British throne, behind her father and elder brother.
Because of the implementation of the Perth Agreement, which replaced male-preference primogeniture with absolute primogeniture, she did not move down the line of succession upon the birth of her younger brother Louis in April 2018, making her the first British princess in history to rank above a brother in the line of succession.



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
  AssignClass (9fc75d6a-fc1b-4ccb-a3f2-045df852ec4f)
 Call ID: 9fc75d6a-fc1b-4ccb-a3f2-045df852ec4f
  Args:
    source: Charlotte_Elizabeth_Diana
    type: :Woman
  AssignClass (b2cfec08-35b1-4583-9aab-0dcec5b0c471)
 Call ID: b2cfec08-35b1-4583-9aab-0dcec5b0c471
  Args:
    source: Charlotte_Elizabeth_Diana
    type: :Person
  AddLiteral (6f5a4d01-6f5d-4b76-96ae-3124ae6d0442)
 Call ID: 6f5a4d01-6f5d-4b76-96ae-3124ae6d0442
  Args:
    source: Charlotte_Elizabeth_Diana
    relation: :hasBirthYear
    literal_value: 2015
    literal_type: xsd:integer
  AssignClass (a41c2410-b478-4bba-90d5-bcfb42f910ac)
 Call ID: a41c2410-b478-4bba-90d5-bcfb42f910ac
  Args:
    source: William_Prince_of_Wales
    type: :Man
  AssignClass (304527ad-cab0-4c8c-be80-14b410dc6d1c)
 Call ID: 304527ad-cab0-4c8c-be80-14b410dc6d1c
  Args:
    source: William_Prince_of_Wales
    type: :Person
  AssignClass (4ebcd082-67aa-4927-b855-012871de0c50)
 Call ID: 4ebcd082-67aa-4927-b855-012871de0c50
  Args:
    source: Catherine_Princess_of_Wales
    type: :Woman
  AssignClass (54ee3b4e-12a3-44ce-bb1d-6f912095a82f)
 Call ID: 54ee3b4e-12a3-44ce-bb1d-6f912095a82f
  Args:
    source: Catherine_Princess_of_Wales
    type: :Person
  AddTriple (3a473c10-af66-4cf8-8968-569df1ab1d13)
 Call ID: 3a473c10-af66-4cf8-8968-569df1ab1d13
  Args:
    relation: :hasFather
    source: Charlotte_Elizabeth_Diana
    target: William_Prince_of_Wales
  AddTriple (78c56031-204b-425c-8040-5a679f918cbe)
 Call ID: 78c56031-204b-425c-8040-5a679f918cbe
  Args:
    relation: :hasMother
    source: Charlotte_Elizabeth_Diana
    target: Catherine_Princess_of_Wales
  AssignClass (d22b8822-f014-4ebd-8059-3a9bfa7d9b65)
 Call ID: d22b8822-f014-4ebd-8059-3a9bfa7d9b65
  Args:
    source: Charles_III
    type: :Man
  AssignClass (e2a17fb5-9d8d-440e-96f4-e30b70cdf6c0)
 Call ID: e2a17fb5-9d8d-440e-96f4-e30b70cdf6c0
  Args:
    source: Charles_III
    type: :Person
  AssignClass (51f2b03b-f7e5-4dce-a5bc-5f7ce9d31985)
 Call ID: 51f2b03b-f7e5-4dce-a5bc-5f7ce9d31985
  Args:
    source: Diana_Princess_of_Wales
    type: :Woman
  AssignClass (b453036f-1346-4758-b8f0-27bd77685441)
 Call ID: b453036f-1346-4758-b8f0-27bd77685441
  Args:
    source: Diana_Princess_of_Wales
    type: :Person
  AssignClass (a594f68c-7546-4d4f-b1eb-e79f95a8ca3e)
 Call ID: a594f68c-7546-4d4f-b1eb-e79f95a8ca3e
  Args:
    source: George
    type: :Man
  AssignClass (5ebf6649-34b5-4884-9a9e-0e9328704834)
 Call ID: 5ebf6649-34b5-4884-9a9e-0e9328704834
  Args:
    source: George
    type: :Person
  AssignClass (2a17291d-a5cd-4312-843d-eb0fd701351f)
 Call ID: 2a17291d-a5cd-4312-843d-eb0fd701351f
  Args:
    source: Louis
    type: :Man
  AssignClass (b2b09e79-0594-47ab-87cd-75fe61435650)
 Call ID: b2b09e79-0594-47ab-87cd-75fe61435650
  Args:
    source: Louis
    type: :Person
  AddTriple (96201851-9274-4703-8a38-2dabb8d5a40b)
 Call ID: 96201851-9274-4703-8a38-2dabb8d5a40b
  Args:
    target: George
    relation: :isSiblingOf
    source: Charlotte_Elizabeth_Diana
  AddTriple (63885f00-8856-462c-88ec-57cafa31edf8)
 Call ID: 63885f00-8856-462c-88ec-57cafa31edf8
  Args:
    target: Louis
    relation: :isSiblingOf
    source: Charlotte_Elizabeth_Diana
  AddTriple (472ee13d-c8d3-4c2a-8370-e144af8f28f2)
 Call ID: 472ee13d-c8d3-4c2a-8370-e144af8f28f2
  Args:
    source: George
    relation: :hasFather
    target: William_Prince_of_Wales
  AddTriple (47244952-3a41-4731-a14b-ecd9ee29ff28)
 Call ID: 47244952-3a41-4731-a14b-ecd9ee29ff28
  Args:
    source: George
    relation: :hasMother
    target: Catherine_Princess_of_Wales
  AddTriple (42bbd274-b9c2-4bf1-b1de-7de5f23fc3cc)
 Call ID: 42bbd274-b9c2-4bf1-b1de-7de5f23fc3cc
  Args:
    target: William_Prince_of_Wales
    source: Louis
    relation: :hasFather
  AddTriple (64ff1ce2-a7b6-4584-a878-4f2fc1193f25)
 Call ID: 64ff1ce2-a7b6-4584-a878-4f2fc1193f25
  Args:
    source: Louis
    relation: :hasMother
    target: Catherine_Princess_of_Wales
  AddLiteral (498d06ea-58c0-4aa0-9e79-5f2bb3bae094)
 Call ID: 498d06ea-58c0-4aa0-9e79-5f2bb3bae094
  Args:
    relation: :knownAs
    source: Charlotte_Elizabeth_Diana
    literal_value: Charlotte Cambridge
    literal_type: xsd:string
  Finish (50bf5f26-ada6-47ac-9787-1d4ce9ee4fc6)
 Call ID: 50bf5f26-ada6-47ac-9787-1d4ce9ee4fc6
  Args: