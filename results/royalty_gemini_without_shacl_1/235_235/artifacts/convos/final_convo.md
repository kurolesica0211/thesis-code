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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Floris Frederik Martijn of Orange-Nassau, van Vollenhoven (born 10 April 1975) is the fourth and youngest son of Princess Margriet of the Netherlands and Pieter van Vollenhoven.
Prince Floris has three older brothers: Prince Maurits, Prince Bernhard, Prince Pieter-Christiaan


Marriage and children

Prince Floris announced his engagement to Aimée Söhngen, the daughter of Hans Söhngen and Eleonoor Stammeijer, on 25 February 2005.
Prince Floris had been 10th in the line of succession to the Dutch throne but decided not to seek parliamentary approval for his marriage, as would be required in the Netherlands.
Prince Floris and Princess Aimée's first child, Magali Margriet Eleonoor van Vollenhoven, was born at VU University Medical Center in Amsterdam on 9 October 2007.
She is named for Aimée's sister, Magali Söhngen, and her mother Eleonoor, as well as Princess Margriet.
Their second child, Eliane Sophia Carolina van Vollenhoven, was born at VU University Medical Center in Amsterdam on 5 July 2009.
Their third child, a son named Willem Jan Johannes Pieter Floris, was born at HMC Bronovo  in The Hague on 1 July 2013.
Ancestry

References

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
  AssignClass (04eca753-b429-4a25-a680-e15da2af2cbe)
 Call ID: 04eca753-b429-4a25-a680-e15da2af2cbe
  Args:
    type: :Woman
    source: :Princess_Beatrix
  AssignClass (19e86da6-eb9b-4c57-83d2-776f2ea89b6d)
 Call ID: 19e86da6-eb9b-4c57-83d2-776f2ea89b6d
  Args:
    source: :Princess_Margriet
    type: :Woman
  AssignClass (23975363-f256-4dfb-a6a4-e9ae1db7850b)
 Call ID: 23975363-f256-4dfb-a6a4-e9ae1db7850b
  Args:
    source: :Pieter_van_Vollenhoven
    type: :Man
  AssignClass (7d6fa8f4-f5cc-417c-b0d5-0239a4dd3834)
 Call ID: 7d6fa8f4-f5cc-417c-b0d5-0239a4dd3834
  Args:
    source: :Prince_Floris_van_Vollenhoven
    type: :Man
  AssignClass (47df8609-6535-4fce-86b9-e92880bad487)
 Call ID: 47df8609-6535-4fce-86b9-e92880bad487
  Args:
    source: :Prince_Maurits
    type: :Man
  AssignClass (b5521386-219b-4185-803c-a2cf07deec9b)
 Call ID: b5521386-219b-4185-803c-a2cf07deec9b
  Args:
    source: :Prince_Bernhard
    type: :Man
  AssignClass (41ca7b29-ef7a-4fd7-9e0f-f84ff4e7594e)
 Call ID: 41ca7b29-ef7a-4fd7-9e0f-f84ff4e7594e
  Args:
    source: :Prince_Pieter_Christiaan
    type: :Man
  AssignClass (d5534f3d-e387-4fbd-b8d2-c30272284873)
 Call ID: d5534f3d-e387-4fbd-b8d2-c30272284873
  Args:
    type: :Woman
    source: :Aimee_Sohngen
  AssignClass (5290786f-2386-4e9d-bc01-8b72554d582b)
 Call ID: 5290786f-2386-4e9d-bc01-8b72554d582b
  Args:
    type: :Man
    source: :Hans_Sohngen
  AssignClass (9f88fd64-a38a-47ed-a1cb-c6a8c5fc4f9b)
 Call ID: 9f88fd64-a38a-47ed-a1cb-c6a8c5fc4f9b
  Args:
    type: :Woman
    source: :Eleonoor_Stammeijer
  AssignClass (b1b39e28-709a-4853-9cbd-7c08eef01c8a)
 Call ID: b1b39e28-709a-4853-9cbd-7c08eef01c8a
  Args:
    source: :Magali_Sohngen
    type: :Woman
  AssignClass (abaa9715-5233-4ae3-a53c-a3f89262e8a2)
 Call ID: abaa9715-5233-4ae3-a53c-a3f89262e8a2
  Args:
    source: :Magali_van_Vollenhoven
    type: :Woman
  AssignClass (3d400ad4-b3d4-426e-8673-748cde8c3300)
 Call ID: 3d400ad4-b3d4-426e-8673-748cde8c3300
  Args:
    source: :Eliane_van_Vollenhoven
    type: :Woman
  AssignClass (43933cbd-f05f-45ec-902f-8a7c174f1a07)
 Call ID: 43933cbd-f05f-45ec-902f-8a7c174f1a07
  Args:
    source: :Willem_Jan_van_Vollenhoven
    type: :Man
  AddTriple (26dd24ef-aa45-4504-ac9a-1c0269a4ab87)
 Call ID: 26dd24ef-aa45-4504-ac9a-1c0269a4ab87
  Args:
    target: :Pieter_van_Vollenhoven
    relation: :hasFather
    source: :Prince_Floris_van_Vollenhoven
  AddTriple (02f27475-56fa-4c15-b7e9-de51d6a10732)
 Call ID: 02f27475-56fa-4c15-b7e9-de51d6a10732
  Args:
    relation: :hasMother
    target: :Princess_Margriet
    source: :Prince_Floris_van_Vollenhoven
  AddTriple (7685c67d-f9ac-4209-8723-7324dbd6be65)
 Call ID: 7685c67d-f9ac-4209-8723-7324dbd6be65
  Args:
    source: :Prince_Floris_van_Vollenhoven
    target: :Prince_Maurits
    relation: :hasBrother
  AddTriple (dc0100f9-6f99-40e1-bcfb-d4dc23e5ba6c)
 Call ID: dc0100f9-6f99-40e1-bcfb-d4dc23e5ba6c
  Args:
    relation: :hasBrother
    target: :Prince_Bernhard
    source: :Prince_Floris_van_Vollenhoven
  AddTriple (b3e1436b-7f2f-4df8-a4e5-571c100fa0ee)
 Call ID: b3e1436b-7f2f-4df8-a4e5-571c100fa0ee
  Args:
    source: :Prince_Floris_van_Vollenhoven
    target: :Prince_Pieter_Christiaan
    relation: :hasBrother
  AddLiteral (78c19e1e-a081-47d2-ba06-0ab45d83a9c0)
 Call ID: 78c19e1e-a081-47d2-ba06-0ab45d83a9c0
  Args:
    literal_value: 1975
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Prince_Floris_van_Vollenhoven
  AddTriple (83c50cfe-6f6b-4f94-b3ea-77658b60562a)
 Call ID: 83c50cfe-6f6b-4f94-b3ea-77658b60562a
  Args:
    relation: :hasFather
    target: :Hans_Sohngen
    source: :Aimee_Sohngen
  AddTriple (c2e2766b-04e5-4ca4-a908-86fc280fa3a9)
 Call ID: c2e2766b-04e5-4ca4-a908-86fc280fa3a9
  Args:
    source: :Aimee_Sohngen
    target: :Eleonoor_Stammeijer
    relation: :hasMother
  AddTriple (51edce88-a316-4fb1-836e-2b038ef376ac)
 Call ID: 51edce88-a316-4fb1-836e-2b038ef376ac
  Args:
    source: :Aimee_Sohngen
    target: :Magali_Sohngen
    relation: :hasSister
  AddTriple (2116ef4c-f9bf-406a-99fe-4126b6ed3f79)
 Call ID: 2116ef4c-f9bf-406a-99fe-4126b6ed3f79
  Args:
    target: :Prince_Floris_van_Vollenhoven
    relation: :hasFather
    source: :Magali_van_Vollenhoven
  AddTriple (35c4e77c-855a-457a-b445-bdc1c6f6d217)
 Call ID: 35c4e77c-855a-457a-b445-bdc1c6f6d217
  Args:
    target: :Aimee_Sohngen
    relation: :hasMother
    source: :Magali_van_Vollenhoven
  AddTriple (c1d79262-9721-4054-bc50-f7edd00597da)
 Call ID: c1d79262-9721-4054-bc50-f7edd00597da
  Args:
    source: :Eliane_van_Vollenhoven
    relation: :hasFather
    target: :Prince_Floris_van_Vollenhoven
  AddTriple (3d83beac-48f8-4037-b64c-21b2e40cf45a)
 Call ID: 3d83beac-48f8-4037-b64c-21b2e40cf45a
  Args:
    source: :Eliane_van_Vollenhoven
    relation: :hasMother
    target: :Aimee_Sohngen
  AddTriple (8f3520c8-262d-4939-87a8-83bd7d909768)
 Call ID: 8f3520c8-262d-4939-87a8-83bd7d909768
  Args:
    source: :Willem_Jan_van_Vollenhoven
    target: :Prince_Floris_van_Vollenhoven
    relation: :hasFather
  AddTriple (4d6abb97-783f-49cd-831a-7ac16aadbb0a)
 Call ID: 4d6abb97-783f-49cd-831a-7ac16aadbb0a
  Args:
    source: :Willem_Jan_van_Vollenhoven
    relation: :hasMother
    target: :Aimee_Sohngen
  Finish (13d12c24-840d-433c-ac75-29112be3ea3f)
 Call ID: 13d12c24-840d-433c-ac75-29112be3ea3f
  Args: