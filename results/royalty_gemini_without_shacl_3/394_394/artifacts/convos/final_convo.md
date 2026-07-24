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
Prince Bernhard of Lippe (Bernhard Kasimir Wilhelm Friedrich Gustav Heinrich Eduard; 26 August 1872 – 19 June 1934) was a member of the Lippe-Biesterfeld line of the House of Lippe.
He was the father of Prince Bernhard of Lippe-Biesterfeld, the prince consort of Queen Juliana of the Netherlands.
Biography

Prince Bernhard of Lippe, born as Count of Lippe-Biesterfeld in Oberkassel on 26 August 1872, was the 2nd son of Ernest II, Count of Lippe-Biesterfeld, regent (1897–1904) of Principality of Lippe, and his wife Countess Karoline von Wartensleben.
He was a younger brother of Leopold IV, Prince of Lippe, who succeeded as reigning Prince of Lippe in 1905.
The Lippe-Biesterfeld family had lived at Oberkassel, Bonn, ever since 1770, when count Frederick William (1737–1803) had married Elisabeth Johanna, Edle von Meinertzhagen (1752–1811), who inherited a small manor house at Oberkassel where the couple moved from Biesterfeld in 1770, and which became the home to the family for the following 209 years.
The manor house and farm at Biesterfeld were demolished around 1820.
Prince Bernhard acquired the Reckenwalde castle in eastern Brandenburg (today Wojnowo, Poland), the family's new estate, where his children grew up.
On 4 March 1909, Bernhard entered into a morganatic marriage with Baroness Armgard von Sierstorpff-Cramm, widowed Countess von Oeynhausen.
Before this marriage, his wife was granted the title Countess of Biesterfeld (Gräfin von Biesterfeld) on 8 February 1909.
She and her two sons Bernhard and Aschwin were created Princess (Prince) of Lippe-Biesterfeld (Prinzessin (Prinz) zur Lippe-Biesterfeld) on 24 February 1916 with the style Serene Highness, which brought their children into a more senior place in the line of succession, in which they hitherto had been the very last.
The suffix Biesterfeld was revived to mark the beginning of a new cadet line.
Bernhard died in Munich, aged 61.



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
  AssignClass (35185208-57f3-4d80-944f-a3d59e744273)
 Call ID: 35185208-57f3-4d80-944f-a3d59e744273
  Args:
    source: Bernhard_of_Lippe
    type: :Man
  AssignClass (994cd100-5522-462c-99af-3846995ccab3)
 Call ID: 994cd100-5522-462c-99af-3846995ccab3
  Args:
    source: Bernhard_of_Lippe
    type: :Person
  AddLiteral (8a01053e-7591-4fb1-ab30-2478744ee419)
 Call ID: 8a01053e-7591-4fb1-ab30-2478744ee419
  Args:
    source: Bernhard_of_Lippe
    relation: :hasBirthYear
    literal_value: 1872
    literal_type: xsd:integer
  AddLiteral (128f8224-1d98-4598-8c93-3d635d272661)
 Call ID: 128f8224-1d98-4598-8c93-3d635d272661
  Args:
    relation: :hasDeathYear
    source: Bernhard_of_Lippe
    literal_value: 1934
    literal_type: xsd:integer
  AssignClass (f9ba25aa-b924-48c2-b552-e2cdd9a15bd0)
 Call ID: f9ba25aa-b924-48c2-b552-e2cdd9a15bd0
  Args:
    type: :Man
    source: Bernhard_of_Lippe-Biesterfeld
  AssignClass (342e06d1-d59a-4882-b0e9-3954cd3ded5b)
 Call ID: 342e06d1-d59a-4882-b0e9-3954cd3ded5b
  Args:
    type: :Person
    source: Bernhard_of_Lippe-Biesterfeld
  AddTriple (822adb9b-181a-4556-bdc0-e833a1ae2925)
 Call ID: 822adb9b-181a-4556-bdc0-e833a1ae2925
  Args:
    target: Bernhard_of_Lippe
    relation: :isSonOf
    source: Bernhard_of_Lippe-Biesterfeld
  AssignClass (bba43dcf-2310-4512-a2f4-25713c9c2c9e)
 Call ID: bba43dcf-2310-4512-a2f4-25713c9c2c9e
  Args:
    source: Ernest_II_Count_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (f319755c-b620-48c0-a2a9-c2751ece92a9)
 Call ID: f319755c-b620-48c0-a2a9-c2751ece92a9
  Args:
    type: :Person
    source: Ernest_II_Count_of_Lippe-Biesterfeld
  AssignClass (39d6fb66-a0aa-42dc-9e7a-09b773470b37)
 Call ID: 39d6fb66-a0aa-42dc-9e7a-09b773470b37
  Args:
    type: :Woman
    source: Karoline_von_Wartensleben
  AssignClass (fe7d685a-530e-4fbe-9008-6689a21bc82b)
 Call ID: fe7d685a-530e-4fbe-9008-6689a21bc82b
  Args:
    source: Karoline_von_Wartensleben
    type: :Person
  AddTriple (c952bc08-b9bf-4639-8d8f-0056b70a088b)
 Call ID: c952bc08-b9bf-4639-8d8f-0056b70a088b
  Args:
    relation: :isSonOf
    target: Ernest_II_Count_of_Lippe-Biesterfeld
    source: Bernhard_of_Lippe
  AddTriple (8d1c93c5-7ae6-4ea6-bbf4-64068c646d29)
 Call ID: 8d1c93c5-7ae6-4ea6-bbf4-64068c646d29
  Args:
    relation: :isSonOf
    target: Karoline_von_Wartensleben
    source: Bernhard_of_Lippe
  AssignClass (a15e8034-0277-4180-aefc-794cec852cd3)
 Call ID: a15e8034-0277-4180-aefc-794cec852cd3
  Args:
    type: :Man
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (68e6efcb-716e-44e3-b494-5b08cd6a7346)
 Call ID: 68e6efcb-716e-44e3-b494-5b08cd6a7346
  Args:
    type: :Person
    source: Leopold_IV_Prince_of_Lippe
  AddTriple (6fb6dc8e-cce0-46d8-92cb-9776fba5488e)
 Call ID: 6fb6dc8e-cce0-46d8-92cb-9776fba5488e
  Args:
    source: Bernhard_of_Lippe
    relation: :isSiblingOf
    target: Leopold_IV_Prince_of_Lippe
  AssignClass (fb70dcd2-f5f4-43bb-ab37-31dcd2f8a807)
 Call ID: fb70dcd2-f5f4-43bb-ab37-31dcd2f8a807
  Args:
    type: :Man
    source: Frederick_William
  AssignClass (ad3e7eec-0c2d-47a4-8726-2f4ea0248845)
 Call ID: ad3e7eec-0c2d-47a4-8726-2f4ea0248845
  Args:
    source: Frederick_William
    type: :Person
  AssignClass (ec809484-2c93-4dc2-9670-f48690734148)
 Call ID: ec809484-2c93-4dc2-9670-f48690734148
  Args:
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
    type: :Woman
  AssignClass (d3ae41c7-d087-44c0-9ba9-d7a7970dc50b)
 Call ID: d3ae41c7-d087-44c0-9ba9-d7a7970dc50b
  Args:
    type: :Person
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
  AddTriple (ed0bb4b2-4422-414c-8c1b-5eeb924d6739)
 Call ID: ed0bb4b2-4422-414c-8c1b-5eeb924d6739
  Args:
    relation: :hasMarriageYear
    target: Elisabeth_Johanna_Edle_von_Meinertzhagen
    source: Frederick_William
  AddLiteral (42277f73-6f52-4b90-b184-774398fd6947)
 Call ID: 42277f73-6f52-4b90-b184-774398fd6947
  Args:
    literal_type: xsd:integer
    literal_value: 1770
    relation: :hasMarriageYear
    source: Frederick_William
  AssignClass (41ef189c-4dd2-44d6-a348-c4a0fcfb41a7)
 Call ID: 41ef189c-4dd2-44d6-a348-c4a0fcfb41a7
  Args:
    source: Armgard_von_Sierstorpff-Cramm
    type: :Woman
  AssignClass (ec635135-de00-4996-8042-79ee6160a1c5)
 Call ID: ec635135-de00-4996-8042-79ee6160a1c5
  Args:
    source: Armgard_von_Sierstorpff-Cramm
    type: :Person
  AddLiteral (a6dbe1a4-d1de-431f-9788-ad15d374a201)
 Call ID: a6dbe1a4-d1de-431f-9788-ad15d374a201
  Args:
    relation: :hasMarriageYear
    source: Bernhard_of_Lippe
    literal_type: xsd:integer
    literal_value: 1909
  AddTriple (a6bac651-adee-4d0f-bd10-c1d99ef006a7)
 Call ID: a6bac651-adee-4d0f-bd10-c1d99ef006a7
  Args:
    source: Bernhard_of_Lippe
    relation: :hasRelation
    target: Armgard_von_Sierstorpff-Cramm
  AssignClass (3d6914a7-a25b-4659-af0b-d4e8a670feee)
 Call ID: 3d6914a7-a25b-4659-af0b-d4e8a670feee
  Args:
    type: :Man
    source: Aschwin
  AssignClass (3b54f868-72d6-42d0-b154-29e9965be705)
 Call ID: 3b54f868-72d6-42d0-b154-29e9965be705
  Args:
    type: :Person
    source: Aschwin
  AddTriple (3a7bd898-f66e-4020-ad05-eddb46a6c2a9)
 Call ID: 3a7bd898-f66e-4020-ad05-eddb46a6c2a9
  Args:
    target: Bernhard_of_Lippe
    relation: :isSonOf
    source: Aschwin
  AddTriple (f66bc3e4-e058-4bda-b038-78aed316160d)
 Call ID: f66bc3e4-e058-4bda-b038-78aed316160d
  Args:
    relation: :isSonOf
    target: Armgard_von_Sierstorpff-Cramm
    source: Aschwin
  AddTriple (00b73f38-b3af-43dc-a625-03313f235677)
 Call ID: 00b73f38-b3af-43dc-a625-03313f235677
  Args:
    target: Armgard_von_Sierstorpff-Cramm
    relation: :isSonOf
    source: Bernhard_of_Lippe-Biesterfeld
  Finish (0d971159-2672-4717-b04d-3f095eda6d7e)
 Call ID: 0d971159-2672-4717-b04d-3f095eda6d7e
  Args: