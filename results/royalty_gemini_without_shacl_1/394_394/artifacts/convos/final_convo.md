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
  AssignClass (1c8e39f0-a0d4-47de-b09e-f58f05b51e05)
 Call ID: 1c8e39f0-a0d4-47de-b09e-f58f05b51e05
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe_1872
  AssignClass (6e5e29a3-cf88-4d07-87c0-781178b0b5fd)
 Call ID: 6e5e29a3-cf88-4d07-87c0-781178b0b5fd
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe_1872
  AddLiteral (d48ad5f2-6ce3-4e0f-bc32-80a7e6bc1902)
 Call ID: d48ad5f2-6ce3-4e0f-bc32-80a7e6bc1902
  Args:
    literal_type: xsd:integer
    literal_value: 1872
    source: Prince_Bernhard_of_Lippe_1872
    relation: :hasBirthYear
  AddLiteral (59cdb92e-b4a5-4353-9ad9-9b4d2e4ff76e)
 Call ID: 59cdb92e-b4a5-4353-9ad9-9b4d2e4ff76e
  Args:
    source: Prince_Bernhard_of_Lippe_1872
    literal_type: xsd:integer
    literal_value: 1934
    relation: :hasDeathYear
  AssignClass (8fc4dffc-47c1-42a1-b0b8-495d79994346)
 Call ID: 8fc4dffc-47c1-42a1-b0b8-495d79994346
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe_Biesterfeld_jr
  AssignClass (133334d0-3c84-4e22-bf1a-c90c34fb1cda)
 Call ID: 133334d0-3c84-4e22-bf1a-c90c34fb1cda
  Args:
    source: Prince_Bernhard_of_Lippe_Biesterfeld_jr
    type: :Person
  AddTriple (8c5f2266-cfb9-46e6-ad75-4268ee0ba288)
 Call ID: 8c5f2266-cfb9-46e6-ad75-4268ee0ba288
  Args:
    target: Prince_Bernhard_of_Lippe_1872
    source: Prince_Bernhard_of_Lippe_Biesterfeld_jr
    relation: :isSonOf
  AssignClass (ff60d162-4747-4784-9261-92216bc6484e)
 Call ID: ff60d162-4747-4784-9261-92216bc6484e
  Args:
    type: :Man
    source: Ernest_II_Count_of_Lippe_Biesterfeld
  AssignClass (2857975f-9d70-48b0-898e-00fc02ef8b69)
 Call ID: 2857975f-9d70-48b0-898e-00fc02ef8b69
  Args:
    source: Ernest_II_Count_of_Lippe_Biesterfeld
    type: :Person
  AddTriple (eaf0b718-74b4-43e0-838d-751b25a24ac6)
 Call ID: eaf0b718-74b4-43e0-838d-751b25a24ac6
  Args:
    target: Ernest_II_Count_of_Lippe_Biesterfeld
    source: Prince_Bernhard_of_Lippe_1872
    relation: :isSonOf
  AssignClass (d534656b-40ec-4d25-87f5-06d4477ead0a)
 Call ID: d534656b-40ec-4d25-87f5-06d4477ead0a
  Args:
    type: :Woman
    source: Countess_Karoline_von_Wartensleben
  AssignClass (aa852384-9556-445b-88cd-a4cf0f097510)
 Call ID: aa852384-9556-445b-88cd-a4cf0f097510
  Args:
    type: :Person
    source: Countess_Karoline_von_Wartensleben
  AddTriple (7976e410-8686-42f6-87d9-216e6fc0330e)
 Call ID: 7976e410-8686-42f6-87d9-216e6fc0330e
  Args:
    relation: :isSonOf
    source: Prince_Bernhard_of_Lippe_1872
    target: Countess_Karoline_von_Wartensleben
  AssignClass (d829d233-e555-464a-9431-07f4286a2871)
 Call ID: d829d233-e555-464a-9431-07f4286a2871
  Args:
    type: :Man
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (282e785e-7538-4c8a-9e6c-9e3ea37723c9)
 Call ID: 282e785e-7538-4c8a-9e6c-9e3ea37723c9
  Args:
    source: Leopold_IV_Prince_of_Lippe
    type: :Person
  AddTriple (fcd20579-fe64-4a09-b43e-31b759624688)
 Call ID: fcd20579-fe64-4a09-b43e-31b759624688
  Args:
    target: Leopold_IV_Prince_of_Lippe
    relation: :isBrotherOf
    source: Prince_Bernhard_of_Lippe_1872
  AssignClass (e86fec34-c7e4-4599-a17f-b3927d769dfe)
 Call ID: e86fec34-c7e4-4599-a17f-b3927d769dfe
  Args:
    type: :Man
    source: Frederick_William_Count_of_Lippe_Biesterfeld
  AssignClass (0c3717e0-d3b7-4833-b311-c671d7382866)
 Call ID: 0c3717e0-d3b7-4833-b311-c671d7382866
  Args:
    type: :Person
    source: Frederick_William_Count_of_Lippe_Biesterfeld
  AssignClass (d919ebb6-14e6-4eb4-9ed4-8d75f7063a73)
 Call ID: d919ebb6-14e6-4eb4-9ed4-8d75f7063a73
  Args:
    type: :Woman
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
  AssignClass (8017a7fb-db18-4138-9773-406a8805e736)
 Call ID: 8017a7fb-db18-4138-9773-406a8805e736
  Args:
    source: Elisabeth_Johanna_Edle_von_Meinertzhagen
    type: :Person
  AddLiteral (f1f6c8bb-6831-451a-a84c-1edff6d52845)
 Call ID: f1f6c8bb-6831-451a-a84c-1edff6d52845
  Args:
    source: Frederick_William_Count_of_Lippe_Biesterfeld
    literal_value: 1770
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (e2f28b44-f789-4541-9492-28c8549e4885)
 Call ID: e2f28b44-f789-4541-9492-28c8549e4885
  Args:
    type: :Woman
    source: Baroness_Armgard_von_Sierstorpff_Cramm
  AssignClass (f39ebaf8-44b7-4212-a734-aa11819f057b)
 Call ID: f39ebaf8-44b7-4212-a734-aa11819f057b
  Args:
    type: :Person
    source: Baroness_Armgard_von_Sierstorpff_Cramm
  AddLiteral (8d5d08e6-855e-4fa7-b3b3-b472c1ad4e87)
 Call ID: 8d5d08e6-855e-4fa7-b3b3-b472c1ad4e87
  Args:
    literal_type: xsd:integer
    literal_value: 1909
    source: Prince_Bernhard_of_Lippe_1872
    relation: :hasMarriageYear
  AssignClass (1ee9063c-d22a-40ff-9555-0215412b57ed)
 Call ID: 1ee9063c-d22a-40ff-9555-0215412b57ed
  Args:
    source: Aschwin_of_Lippe_Biesterfeld
    type: :Man
  AssignClass (e4e2d742-d5db-47ca-85df-d30dea7b14c1)
 Call ID: e4e2d742-d5db-47ca-85df-d30dea7b14c1
  Args:
    type: :Person
    source: Aschwin_of_Lippe_Biesterfeld
  AddTriple (36e8d607-4b89-4475-8d2f-44bdedc91ea1)
 Call ID: 36e8d607-4b89-4475-8d2f-44bdedc91ea1
  Args:
    source: Aschwin_of_Lippe_Biesterfeld
    relation: :isSonOf
    target: Prince_Bernhard_of_Lippe_1872
  AddTriple (dc07b256-9ca9-4f41-88b3-76fb84575e0a)
 Call ID: dc07b256-9ca9-4f41-88b3-76fb84575e0a
  Args:
    target: Baroness_Armgard_von_Sierstorpff_Cramm
    relation: :isSonOf
    source: Aschwin_of_Lippe_Biesterfeld
  Finish (297559f9-8024-4321-a634-af5699960951)
 Call ID: 297559f9-8024-4321-a634-af5699960951
  Args: