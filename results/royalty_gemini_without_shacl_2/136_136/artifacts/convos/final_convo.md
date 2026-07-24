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
Prince Alexander Ferdinand Albrecht Achilles Wilhelm Joseph Viktor Karl Feodor of Prussia (26 December 1912 – 12 June 1985) was the only son of Prince August Wilhelm of Prussia and Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
Family and early life

Prince Alexander of Prussia was born on 26 December 1912 to Prince August Wilhelm of Prussia and his wife Princess Alexandra Victoria of Schleswig-Holstein-Sonderburg-Glücksburg.
August Wilhelm was a younger son of Kaiser Wilhelm II.
His parents divorced in 1920 and his mother remarried less than two years later; custody of the young prince was awarded to Alexander's father.
Alexander attended the 1932 wedding of the Swedish prince Gustaf Adolf, Duke of Västerbotten with Princess Sibylla of Saxe-Coburg-Gotha in the former duchy of Coburg; it was the first time that a member of the German imperial family had entered the duchy since it became a republic, or specifically a part of Bavaria in November 1919 after the ruling duke, Carl Eduard, had ended his reign on 14 November 1918.
Nazi Party and military career

As of November 1939, Prince Alexander was a first lieutenant in the Air Force Signal Corps, stationed in Wiesbaden.
Like his father, who became a prominent supporter of the Nazi Party, Alexander became an early supporter.
Prince August had secret hopes that Chancellor Adolf Hitler "would one day hoist him or his son Alexander up to the vacant throne of the Kaiser".
The support that father and son gave to the emerging party caused strong disagreements among the Hohenzollerns, with Wilhelm II urging them both to leave the party.
In 1933, Alexander quit the SA and became a private in the German regular army.
Unlike many other German princes, who became the targets of Hitler's mistrust and were removed from their commands in the military, Alexander was the only Hohenzollern allowed to remain at his post.
Marriage

On 19 December 1938 in the Dresden garrison church, Alexander non-dynastically married Armgard Weygand (22 August 1912 – 3 December 2001), daughter of Major Friedrich Weygand and Karla Franziska Oheim.
She was married from 1928 to 1933 to Werner Rosendorff, airman in the German Air Force, and was originally from Wiesbaden, where Alexander Ferdinand was stationed.
They had one son:


Death

Prince Alexander Ferdinand died on 12 June 1985 at Wiesbaden.
}} Media related to Prince Alexander Ferdinand of Prussia at Wikimedia Commons



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
  AssignClass (ab1de32d-c1f7-473a-b20b-50b54dfe9701)
 Call ID: ab1de32d-c1f7-473a-b20b-50b54dfe9701
  Args:
    type: :Man
    source: Prince_Alexander_Ferdinand_of_Prussia
  AssignClass (ab39d962-38ee-44f5-a0c1-afddfc991344)
 Call ID: ab39d962-38ee-44f5-a0c1-afddfc991344
  Args:
    type: :Man
    source: Prince_August_Wilhelm_of_Prussia
  AssignClass (43603713-f3a4-4461-a498-aa4a46b4362c)
 Call ID: 43603713-f3a4-4461-a498-aa4a46b4362c
  Args:
    source: Princess_Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
    type: :Woman
  AssignClass (7e7e2258-92e1-46c6-a6a6-5bdb3acbaa88)
 Call ID: 7e7e2258-92e1-46c6-a6a6-5bdb3acbaa88
  Args:
    type: :Man
    source: Kaiser_Wilhelm_II
  AssignClass (7e5dd6fd-b55c-4705-b715-606188a63fef)
 Call ID: 7e5dd6fd-b55c-4705-b715-606188a63fef
  Args:
    type: :Woman
    source: Armgard_Weygand
  AssignClass (735c0b40-86d1-4f0b-9e5b-983e12b934f9)
 Call ID: 735c0b40-86d1-4f0b-9e5b-983e12b934f9
  Args:
    source: Major_Friedrich_Weygand
    type: :Man
  AssignClass (7b807e26-bc26-421d-aeee-1f3071d8fd41)
 Call ID: 7b807e26-bc26-421d-aeee-1f3071d8fd41
  Args:
    source: Karla_Franziska_Oheim
    type: :Woman
  AssignClass (1d7b0f85-00b3-4a8e-8b72-2bbe910ec9a4)
 Call ID: 1d7b0f85-00b3-4a8e-8b72-2bbe910ec9a4
  Args:
    source: Werner_Rosendorff
    type: :Man
  AddLiteral (c9725fdf-9d99-484d-8a78-dcd2f3c9c818)
 Call ID: c9725fdf-9d99-484d-8a78-dcd2f3c9c818
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Alexander_Ferdinand_of_Prussia
    literal_value: 1912
  AddLiteral (2c8549e6-43c7-449b-acfc-848a4c59d8ab)
 Call ID: 2c8549e6-43c7-449b-acfc-848a4c59d8ab
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Prince_Alexander_Ferdinand_of_Prussia
    literal_value: 1985
  AddTriple (500267b0-e08f-4c5b-abf1-c10d54b87e4b)
 Call ID: 500267b0-e08f-4c5b-abf1-c10d54b87e4b
  Args:
    relation: :hasFather
    source: Prince_Alexander_Ferdinand_of_Prussia
    target: Prince_August_Wilhelm_of_Prussia
  AddTriple (c11058bc-e837-4756-a04a-69691165039f)
 Call ID: c11058bc-e837-4756-a04a-69691165039f
  Args:
    relation: :hasMother
    source: Prince_Alexander_Ferdinand_of_Prussia
    target: Princess_Alexandra_Victoria_of_Schleswig-Holstein-Sonderburg-Glücksburg
  AddTriple (90d972a1-9ec6-45cb-8427-c1d08514ecb4)
 Call ID: 90d972a1-9ec6-45cb-8427-c1d08514ecb4
  Args:
    target: Kaiser_Wilhelm_II
    source: Prince_August_Wilhelm_of_Prussia
    relation: :hasFather
  AddLiteral (7f140107-6f6e-4df6-852b-bb902d763f96)
 Call ID: 7f140107-6f6e-4df6-852b-bb902d763f96
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1938
    source: Prince_Alexander_Ferdinand_of_Prussia
  AddTriple (60eb5792-4b54-4a3a-ba70-d5e544344e6e)
 Call ID: 60eb5792-4b54-4a3a-ba70-d5e544344e6e
  Args:
    relation: :hasRelation
    source: Prince_Alexander_Ferdinand_of_Prussia
    target: Armgard_Weygand
  AddTriple (ae7bd6a5-77d6-47ac-91d3-fac432a95b60)
 Call ID: ae7bd6a5-77d6-47ac-91d3-fac432a95b60
  Args:
    source: Armgard_Weygand
    target: Major_Friedrich_Weygand
    relation: :hasFather
  AddTriple (90a1b1e0-8e0d-4471-8dd0-c887d771579d)
 Call ID: 90a1b1e0-8e0d-4471-8dd0-c887d771579d
  Args:
    relation: :hasMother
    target: Karla_Franziska_Oheim
    source: Armgard_Weygand
  AddLiteral (4085529d-8d33-4060-835f-fd14c3da6337)
 Call ID: 4085529d-8d33-4060-835f-fd14c3da6337
  Args:
    source: Armgard_Weygand
    literal_value: 1912
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (272f34ce-81af-49f5-a175-90b907949c7c)
 Call ID: 272f34ce-81af-49f5-a175-90b907949c7c
  Args:
    source: Armgard_Weygand
    literal_value: 2001
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (518bf251-21b3-40f2-bd30-22dcf50be567)
 Call ID: 518bf251-21b3-40f2-bd30-22dcf50be567
  Args:
    target: Werner_Rosendorff
    source: Armgard_Weygand
    relation: :hasRelation
  Finish (47a20110-5195-473b-87f9-771aad7cd6c4)
 Call ID: 47a20110-5195-473b-87f9-771aad7cd6c4
  Args: